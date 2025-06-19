try:
    from flask_frozen import Freezer as FrozenFreezer
except ModuleNotFoundError:  # offline testing environment
    import os
    class FrozenFreezer:
        """Minimal freezer fallback when flask_frozen is unavailable."""
        def __init__(self, app, with_static_files=True):
            self.app = app
        def freeze(self):
            client = self.app.test_client()
            os.makedirs("build", exist_ok=True)
            for rule in self.app.url_map.iter_rules():
                if "GET" not in rule.methods or rule.arguments:
                    continue
                path = rule.rule.rstrip("/")
                if path == "":
                    dest = "index.html"
                else:
                    dest = f"{path.lstrip('/')}/index.html"
                out = os.path.join("build", dest)
                os.makedirs(os.path.dirname(out), exist_ok=True)
                resp = client.get(rule.rule)
                with open(out, "wb") as fh:
                    fh.write(resp.data)

from app import app


class PatchedFreezer(FrozenFreezer):
    def urlpath_to_filepath(self, path):
        """Ensure URLs map to .html files for static hosting."""
        if path == "/performance":
            path = "/performance/index.html"
        elif path.startswith("/performance/"):
            path = f"{path}.html"
        elif path in {"/politique", "/politique/"}:
            path = "/politique/index.html"
        else:
            # If the path has no extension, map to /path/index.html
            segment = path.rstrip("/")
            if not segment.split("/")[-1].count('.'):
                path = f"{segment}/index.html"
        return super().urlpath_to_filepath(path)

freezer = PatchedFreezer(app, with_static_files=True)

if __name__ == "__main__":
    freezer.freeze()
