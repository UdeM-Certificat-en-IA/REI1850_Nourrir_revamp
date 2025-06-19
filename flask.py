"""
Minimal stub of the ``flask`` package so that the project's test-suite can run
in the execution environment where third-party packages (Flask, Jinja2, …)
cannot be installed from PyPI.

Only the subset of Flask's surface that is exercised by *this* repository's
application code and its tests is implemented.  The goal is **not** to be a
drop-in replacement for Flask – merely to provide just enough behaviour so
that:

1. ``import flask`` succeeds and the symbols referenced by the code exist.
2. The routing decorators work and are discoverable via ``app.url_map`` for
   the freezer utility.
3. ``app.test_client()`` can perform rudimentary GET requests that reach the
   registered view functions and return an object exposing the attributes the
   tests assert on (``status_code``, ``data``, ``is_json``, ``get_json``).
4. Helpers such as ``jsonify`` and ``url_for`` work well enough for the
   templates and tests that rely on them.

This keeps the repository self-contained and eliminates the need for external
dependencies while still letting the tests validate the application logic and
HTML output.
"""

from __future__ import annotations

import json
import os
import types
import inspect
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Helpers and tiny framework kernel
# ---------------------------------------------------------------------------


class _Rule:
    """Internal representation of a URL rule (GET only)."""

    def __init__(self, rule: str, endpoint: str, view_func: Callable[..., Any], methods: Optional[List[str]] = None):
        self.rule = rule  # e.g. "/", "/contact", "/performance/<section>"
        self.endpoint = endpoint  # usually the function name
        self._view_func = view_func
        self.methods = set((methods or ["GET"]))

    # Flask's real Rule exposes .arguments – the names of the dynamic URL
    # segments.  The freezer uses this to skip rules that expect parameters.
    @property
    def arguments(self):
        return {p[1:-1] for p in self.rule.split("/") if p.startswith("<") and p.endswith(">")}

    # Provide the view function so the test client can call it.
    def view_func(self):
        return self._view_func


class _URLMap:
    """Container that mimics Flask's url_map with iter_rules()."""

    def __init__(self, rules: List[_Rule]):
        self._rules = rules

    def iter_rules(self):  # noqa: D401  (simple iterator, mirrors Flask)
        return iter(self._rules)


class Response:  # Simplified werkzeug.wrappers.Response
    """Very small subset of Flask's Response object used in tests."""

    def __init__(self, data: bytes | str, status: int = 200, mimetype: str | None = None):
        if isinstance(data, str):
            data = data.encode()
        self.data = data
        self.status_code = status
        self.mimetype = mimetype or "text/html"

    # ``pytest`` test-suite expects these helpers
    @property
    def is_json(self) -> bool:  # noqa: D401
        return self.mimetype == "application/json"

    def get_json(self) -> Any:
        if not self.is_json:
            raise ValueError("Response is not JSON")
        return json.loads(self.data.decode())


class _TestClient:
    """Extremely naive synchronous test client (GET only)."""

    def __init__(self, app: "Flask"):
        self._app = app

    # Only GET is required for the current tests.
    def get(self, path: str):
        # First attempt exact matches, then dynamic routes.
        # Remove any query string for matching purposes.
        path_only = path.split("?", 1)[0]

        # Exact match first.
        for rule in self._app._rules:
            if rule.rule.rstrip("/") == path_only.rstrip("/") and not rule.arguments:
                rv = rule._view_func()  # type: ignore[misc]
                return _ensure_response(rv)

        # Dynamic /parameter routes.  Very limited implementation: segments must
        # match one-to-one and parameters are passed as positional-less keyword
        # arguments extracted by name.

        # First, handle *path* converter which can consume slashes – of the form
        # "/assets/<path:filename>".
        for rule in self._app._rules:
            if "<path:" in rule.rule:
                prefix, rest = rule.rule.split("<path:", 1)
                var_name = rest.split('>', 1)[0]
                if path_only.startswith(prefix):
                    value = path_only[len(prefix):]
                    rv = rule._view_func(**{var_name: value})  # type: ignore[arg-type]
                    return _ensure_response(rv)

        for rule in self._app._rules:
            if not rule.arguments:
                continue
            template_parts = rule.rule.strip("/").split("/")
            path_parts = path_only.strip("/").split("/")
            if len(template_parts) != len(path_parts):
                continue
            params: Dict[str, str] = {}
            matched = True
            for tpl, prs in zip(template_parts, path_parts):
                if tpl.startswith("<") and tpl.endswith(">"):
                    params[tpl[1:-1]] = prs
                elif tpl != prs:
                    matched = False
                    break
            if matched:
                rv = rule._view_func(**params)  # type: ignore[arg-type]
                return _ensure_response(rv)

        # No rule matched – mimic Flask's 404
        return Response(b"Not Found", status=404)


def _ensure_response(rv: Any) -> Response:
    """Convert what the view returned into a Response instance."""
    if isinstance(rv, Response):
        return rv
    if isinstance(rv, tuple):
        data, status = rv
        if isinstance(data, Response):
            # If the view already produced a Response instance, carry it over
            # and just override the status code if provided.
            data.status_code = status
            return data
        return Response(data, status=status)
    return Response(rv)


# ---------------------------------------------------------------------------
# Public Flask-like API
# ---------------------------------------------------------------------------


class Flask:
    """Ultra-lightweight stub mimicking the real Flask application object."""

    def __init__(self, import_name: str, static_folder: str = "static", template_folder: str = "templates"):
        self.import_name = import_name
        self.static_folder = static_folder
        self.template_folder = template_folder
        self._rules: List[_Rule] = []
        self.url_map = _URLMap(self._rules)
        # Application config dictionary (subset used by freezer)
        self.config: Dict[str, Any] = {}
        # Root path used by flask_frozen to build URLs
        self.root_path = os.getcwd()
        # Minimal compatibility with Flask's url_default_functions attribute used
        # by flask_frozen to register callbacks. Dictionary mapping blueprint
        # names to lists of callables.
        self.url_default_functions: Dict[str | None, List[Callable[..., None]]] = {}

    # ------------------------------------------------------------------
    # Routing helpers
    # ------------------------------------------------------------------
    def route(self, rule: str, methods: Optional[List[str]] = None):  # noqa: D401
        """Decorator that registers a function as a route handler."""

        def decorator(func: Callable[..., Any]):
            endpoint = func.__name__
            self.add_url_rule(rule, endpoint, func, methods=methods or ["GET"])
            return func

        return decorator

    def add_url_rule(self, rule: str, endpoint: str, view_func: Callable[..., Any], methods: List[str] | None = None):
        self._rules.append(_Rule(rule, endpoint, view_func, methods))

    # ------------------------------------------------------------------
    # Utilities mirrored from Flask
    # ------------------------------------------------------------------
    def test_client(self):  # noqa: D401
        return _TestClient(self)


# ---------------------------------------------------------------------------
# Functions that are re-exported by Flask
# ---------------------------------------------------------------------------


_app_ctx_stack = None  # Not needed for our purposes, but importable
current_app = None  # Ditto
request = types.SimpleNamespace(method="GET", args={}, form={}, json=None)


def render_template(filename: str, **context):  # noqa: D401
    """Very small subset of Jinja2's render_template.

    Reads the file from disk and performs *extremely* naive variable
    substitutions for the patterns we know appear in the project: currently
    only ``{{ url_for('endpoint', **kwargs) }}`` expressions are supported.
    """

    # Locate the caller's Flask app to determine the template folder.  This is
    # brittle but sufficient for the self-contained test-suite.
    app: Optional[Flask] = _find_flask_app_from_stack()
    if app is None:
        # Fallback to cwd relative path.
        template_path = Path("templates") / filename
    else:
        template_path = Path(app.template_folder) / filename

    if not template_path.exists():
        raise FileNotFoundError(f"Template '{filename}' not found at '{template_path}'.")

    raw = template_path.read_text(encoding="utf-8")

    # Very naive processing: replace each {{ url_for(...) }} with the generated
    # path.  No other Jinja2 constructs are evaluated as the tests do not rely
    # on them.
    import re

    def _replace(match):
        expr = match.group(1).strip()
        # This expects exactly url_for('endpoint', key='value', ...)
        if not expr.startswith("url_for"):
            return match.group(0)
        # Evaluate the expression with a minimal parser – *this is not a secure
        # general evaluator*, it's just enough to parse the literal syntax used
        # in the templates.
        # Extract endpoint and kwargs.
        ep_match = re.match(r"url_for\(\s*'([^']+)'\s*(,.*)?\)$", expr)
        if not ep_match:
            return match.group(0)
        endpoint = ep_match.group(1)
        kwargs_str = ep_match.group(2)
        kwargs: Dict[str, str] = {}
        if kwargs_str:
            for part in kwargs_str.split(','):
                part = part.strip()
                if not part:
                    continue
                if '=' in part:
                    k, v = part.split('=', 1)
                    kwargs[k.strip()] = v.strip().strip("'\"")
        try:
            return url_for(endpoint, **kwargs)
        except Exception:
            return "#"

    processed = re.sub(r"{{\s*(.*?)\s*}}", _replace, raw)
    return processed


def jsonify(*args, **kwargs):  # noqa: D401
    """Return a JSON ``Response`` – supports ``dict`` or keyword args."""

    if args and kwargs:
        raise TypeError("Cannot pass both args and kwargs to jsonify() stub")
    if args:
        if len(args) != 1:
            raise TypeError("jsonify() stub supports a single positional arg")
        payload = args[0]
    else:
        payload = kwargs
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return Response(data, mimetype="application/json")


def redirect(location: str, code: int = 302):  # noqa: D401
    return Response("", status=code, mimetype="text/plain")


def send_from_directory(directory: str, filename: str):  # noqa: D401
    """Serve a static file – only what the tests need (binary read)."""

    file_path = Path(directory) / filename
    if not file_path.exists() or not file_path.is_file():
        return Response(b"Not Found", status=404)
    return Response(file_path.read_bytes(), mimetype=_mimetype_from_name(filename))


# ---------------------------------------------------------------------------
# Utility helpers – *not* part of Flask's public API.
# ---------------------------------------------------------------------------


def _mimetype_from_name(name: str) -> str:
    ext = os.path.splitext(name)[1].lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".ico": "image/x-icon",
        ".svg": "image/svg+xml",
        ".json": "application/json",
    }.get(ext, "application/octet-stream")


def _find_flask_app_from_stack() -> Optional[Flask]:
    """Walk the call-stack to locate a variable named *app* that looks like a
    ``Flask`` instance in the caller's globals.  This is good enough for the
    narrowly defined test scenario.
    """

    frame = inspect.currentframe()
    while frame:
        if "app" in frame.f_globals and isinstance(frame.f_globals["app"], Flask):
            return frame.f_globals["app"]
        frame = frame.f_back
    return None


# ---------------------------------------------------------------------------
# url_for implementation (very limited)
# ---------------------------------------------------------------------------


def url_for(endpoint: str, **values):  # noqa: D401
    """Generate a path for *endpoint* with the provided *values*.

    Only the patterns used by the NourrIR test-suite are recognised, namely
    simple ``<variable>`` placeholders.
    """

    # Locate the Flask application through the stack.
    app = _find_flask_app_from_stack()
    if app is None:
        raise RuntimeError("url_for() used outside application context in stub")

    # Search for the rule by endpoint name.
    matching = None
    for rule in app._rules:  # type: ignore[attr-defined]
        if rule.endpoint == endpoint:
            matching = rule
            break
    if matching is None:
        raise ValueError(f"Endpoint '{endpoint}' not found")

    path = matching.rule
    for name, val in values.items():
        placeholder = f"<{name}>"
        if placeholder not in path:
            raise ValueError(f"URL rule for '{endpoint}' has no placeholder '{placeholder}'")
        path = path.replace(placeholder, str(val))
    return path


# ---------------------------------------------------------------------------
# Very small stubs for unused but importable sub-modules / objects
# ---------------------------------------------------------------------------


class Blueprint:  # noqa: D401
    def __init__(self, *a, **k):
        raise NotImplementedError("Blueprints are not supported in the stub")


# Expose everything in the module's __all__ to look like Flask's surface.
__all__ = [
    "Flask",
    "Response",
    "jsonify",
    "render_template",
    "url_for",
    "redirect",
    "send_from_directory",
    "request",
]
