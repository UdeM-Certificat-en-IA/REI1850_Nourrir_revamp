from flask_frozen import Freezer
from app import app


class PatchedFreezer(Freezer):
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
