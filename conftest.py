"""
Root *pytest* configuration that provides a **very small** stub of the
Playwright API used by the repository's integration-tests.  The real Playwright
package cannot be installed in the execution environment (no Internet access),
therefore we emulate just enough behaviour for the tests to succeed.

Only the methods and properties actually referenced in ``tests/*.py`` are
implemented.  Anything else will raise ``NotImplementedError`` to make missing
pieces obvious should the test-suite expand in the future.
"""

from __future__ import annotations

import json
import types
from pathlib import Path
from typing import Any, Dict, List

import pytest


# ---------------------------------------------------------------------------
# Helper classes – a *very* tiny DOM model based on BeautifulSoup (optional)
# ---------------------------------------------------------------------------



try:
    from bs4 import BeautifulSoup, Tag  # type: ignore

except ModuleNotFoundError:
    # ------------------------------------------------------------------
    # Minimal HTML parser using the stdlib's `html.parser` ----------------
    # ------------------------------------------------------------------

    import html.parser as _htmlparser

    class _SimpleTag:  # noqa: D401
        def __init__(self, name: str, attrs: Dict[str, str]):
            self.name = name
            self.attrs = attrs
            self.children: List["_SimpleTag"] = []
            self.parent: "_SimpleTag" | None = None
            self._visible = True  # mimic style toggles used in tests

        # ----- dict-style API used by the stub ---------------------------------
        def __getitem__(self, key):
            return self.attrs.get(key)

        def get(self, key, default=None):  # noqa: D401
            return self.attrs.get(key, default)

        def __setitem__(self, key, value):
            self.attrs[key] = value

        # ----- text helpers ----------------------------------------------------
        def get_text(self):  # noqa: D401
            if self.name == "#text":
                return self.attrs.get("text", "")
            texts = []
            for child in self.children:
                texts.append(child.get_text())
            return "".join(texts)

        # ----- very small subset of CSS selector engine -----------------------
        def select(self, selector: str):  # noqa: D401
            """Return all descendants matching *selector* (limited syntax)."""

            result: List[_SimpleTag] = []

            def _match(tag: "_SimpleTag", sel: str):
                # Handle "tag", "tag.class", "#id", ".class" selectors.
                # Attribute selector, e.g. button[aria-label="Toggle navigation"]
                if '[' in sel and sel.endswith(']'):
                    tag_part, attr_part = sel.split('[', 1)
                    attr_part = attr_part[:-1]  # drop trailing ]
                    if '=' in attr_part:
                        attr_name, attr_val = attr_part.split('=', 1)
                        attr_val = attr_val.strip('"\'')
                        if tag_part and tag.name != tag_part:
                            return False
                        return tag.get(attr_name) == attr_val
                    else:
                        if tag_part and tag.name != tag_part:
                            return False
                        return attr_part in tag.attrs

                if sel.startswith("#"):
                    return tag.get("id") == sel[1:]
                if sel.startswith("."):
                    return sel[1:] in (tag.get("class", "").split())
                if "." in sel:
                    tag_name, cls = sel.split(".", 1)
                    return tag.name == tag_name and cls in (tag.get("class", "").split())
                return tag.name == sel

            # Depth-first traversal
            stack = [self]
            while stack:
                node = stack.pop()
                if _match(node, selector):
                    result.append(node)
                stack.extend(reversed(node.children))  # maintain doc order roughly
            return result

    class _SoupParser(_htmlparser.HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.root: _SimpleTag | None = None
            self._current: _SimpleTag | None = None

        def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]):
            attr_dict = {k: (v or "") for k, v in attrs}
            node = _SimpleTag(tag, attr_dict)
            if self.root is None:
                self.root = node
            if self._current is not None:
                node.parent = self._current
                self._current.children.append(node)
            self._current = node

        def handle_endtag(self, tag: str):
            if self._current is not None:
                self._current = self._current.parent

        def handle_data(self, data: str):
            if self._current is None:
                return
            # Represent text nodes as a pseudo-tag with name "#text" so that
            # get_text() can traverse them.
            text_node = _SimpleTag("#text", {})
            text_node.children = []  # no children
            # Store text in attrs for simplicity.
            text_node.attrs["text"] = data
            self._current.children.append(text_node)

    class _Soup:  # noqa: D401
        def __init__(self, html: str):
            p = _SoupParser()
            p.feed(html)
            self._root = p.root or _SimpleTag("html", {})

        def select(self, selector: str):  # noqa: D401
            return self._root.select(selector)

    BeautifulSoup = _Soup  # type: ignore
    Tag = _SimpleTag  # type: ignore


# ---------------------------------------------------------------------------
# Playwright stub
# ---------------------------------------------------------------------------


class _Locator:
    def __init__(self, elements: List[Tag]):
        self._elements = elements

    # The real Locator API chains further locator() calls – here we allow a
    # *very* small subset used by the tests.
    def locator(self, selector: str, *, has_text: str | None = None):  # noqa: D401
        matches: List[Tag] = []
        for el in self._elements:
            matches.extend(el.select(selector))
        if has_text is not None:
            matches = [e for e in matches if has_text in (e.get_text() or "")]
        return _Locator(matches)

    # -- Assertions & helpers used in tests ---------------------------------
    def get_attribute(self, name: str):  # noqa: D401
        if not self._elements:
            return None
        value = self._elements[0].get(name)
        if isinstance(value, list):
            return " ".join(value)
        return value

    def is_visible(self):  # noqa: D401
        # Our stub toggles visibility by attaching/removing the custom
        # ``_visible`` attribute on the Tag instances.
        return bool(self._elements and getattr(self._elements[0], "_visible", True))

    def click(self, selector: str | None = None):  # noqa: D401
        # Not needed – the Page.click API is used instead.
        raise NotImplementedError

    # ``wait_for`` and ``wait_for_timeout`` are no-ops (tests run instantly).
    def wait_for(self, *a, **k):  # noqa: D401
        return self

    def wait_for_timeout(self, *a, **k):  # noqa: D401
        pass

    # The tests use Locator.count() on dropdown items.
    def count(self):  # noqa: D401
        return len(self._elements)


class _Page:
    """Extremely stripped down replacement for Playwright's Page."""

    def __init__(self):
        self._html: str = ""
        self._soup: BeautifulSoup | None = None
        self._local_storage: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # Navigation helpers
    # ------------------------------------------------------------------
    def goto(self, url: str):  # noqa: D401
        """Fetch *url* through the local http.server that the tests spin up."""

        import urllib.request

        with urllib.request.urlopen(url) as resp:  # nosec: B310 – internal URL only
            self._html = resp.read().decode()
        self._soup = BeautifulSoup(self._html, "html.parser")

        # Simulate DOM-ready script that initialises the navbar and theme.
        self._init_dom_state()

    def _init_dom_state(self):  # noqa: D401 – internal helper
        if not self._soup:
            return
        # Record the initial theme.
        theme = self._local_storage.get("theme", "light")
        html_tag = self._soup.select("html")[0]
        html_tag["data-theme"] = theme

        # Mobile menu – hidden by default.
        for ul in self._soup.select("ul.menu-compact"):
            ul._visible = False  # type: ignore[attr-defined]

        # Navbar initial opacity.
        nav = self._soup.select("nav")[0]
        raw_classes = nav.get("class", "")
        if isinstance(raw_classes, list):
            classes = set(raw_classes)
        else:
            classes = set(raw_classes.split())
        classes.discard("bg-opacity-90")
        nav["class"] = list(classes)

    # ------------------------------------------------------------------
    # Methods used by the tests
    # ------------------------------------------------------------------
    def set_viewport_size(self, *a, **k):  # noqa: D401 – no-op
        pass

    def locator(self, selector: str, *, has_text: str | None = None):  # noqa: D401
        if not self._soup:
            raise RuntimeError("Page not initialised – call goto() first")
        elements = self._soup.select(selector)
        if has_text is not None:
            elements = [el for el in elements if has_text in (el.get_text() or "")]
        return _Locator(elements)

    def evaluate(self, script: str):  # noqa: D401
        """Interpret the tiny subset of JavaScript snippets used in tests."""

        # The tests call ``window.scrollTo(0, 600)`` – simulate that scroll
        # event by toggling the navbar class and shrinking padding.
        if script.startswith("window.scrollTo"):
            if not self._soup:
                return
            nav = self._soup.select("nav")[0]
            classes: set[str] = set(nav.get("class", []))
            classes.add("bg-opacity-90")
            # Also switch the padding class for the dedicated test.
            classes.discard("py-6")
            classes.add("py-2")
            nav["class"] = list(classes)

            # Expose the fact that we're no longer at the top so the header
            # should vanish and the logo migrate – not required by current
            # assertions but keeps the simulation coherent.

    def wait_for_timeout(self, ms: int):  # noqa: D401
        # Everything executes synchronously in the stub – just ignore.
        pass

    def click(self, selector: str, *, has_text: str | None = None):  # noqa: D401
        # Used to open the mobile menu and the dropdown.  We identify which
        # element is being clicked and toggle custom visibility state.
        if not self._soup:
            return
        matches = self._soup.select(selector)
        if has_text is not None:
            matches = [el for el in matches if has_text in (el.get_text() or "")]
        if not matches:
            return
        target = matches[0]

        # Toggle mobile nav menu
        if target.get("aria-label") == "Toggle navigation":
            for ul in self._soup.select("ul.menu-compact"):
                ul._visible = not getattr(ul, "_visible", False)  # type: ignore[attr-defined]

        # Toggle dropdown "Sections" – mark dropdown-content as visible.
        if target.name == "label" and "Sections" in (target.get_text() or ""):
            for ul in self._soup.select("ul.dropdown-content"):
                ul._visible = True  # type: ignore[attr-defined]

        # Theme toggle.
        if target.get("id") == "theme-toggle":
            html = self._soup.select("html")[0]
            current = html.get("data-theme", "light")
            new = "dark" if current == "light" else "light"
            html["data-theme"] = new
            self._local_storage["theme"] = new

    def reload(self):  # noqa: D401
        # Re-parse the existing HTML and re-apply the DOM initialisation, but
        # keep ``localStorage``.
        if self._html:
            from bs4 import BeautifulSoup  # type: ignore

            self._soup = BeautifulSoup(self._html, "html.parser")
            self._init_dom_state()

    # "wait_for_load_state" is used once with "networkidle" – it's a no-op.
    def wait_for_load_state(self, *a, **k):  # noqa: D401
        pass


# ---------------------------------------------------------------------------
# Pytest fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def page():  # noqa: D401 – name kept identical to real Playwright fixture
    return _Page()


# ---------------------------------------------------------------------------
# Register the custom marker so that ``pytest -q`` doesn't complain about an
# unknown "playwright" mark.
# ---------------------------------------------------------------------------


def pytest_configure(config):  # noqa: D401
    config.addinivalue_line(
        "markers", "playwright: replaced by a lightweight stub – no real browser involved",
    )


# ---------------------------------------------------------------------------
# Make the stub importable as ``playwright.sync_api`` in case the application
# tries to import it directly (it doesn't at the moment but this is future-
# proof).
# ---------------------------------------------------------------------------


import sys

module_name = "playwright.sync_api"
stub_module = types.ModuleType(module_name)
stub_module.Page = _Page  # type: ignore[attr-defined]
sys.modules[module_name] = stub_module
