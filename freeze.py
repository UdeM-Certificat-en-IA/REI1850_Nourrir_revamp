from flask_frozen import Freezer
from app import app


class PatchedFreezer(Freezer):
    def urlpath_to_filepath(self, path):
        if path == "/performance":
            path = "/performance/index.html"
        elif path.startswith("/performance/"):
            path = f"{path}.html"
        return super().urlpath_to_filepath(path)

freezer = PatchedFreezer(app, with_static_files=True)

if __name__ == "__main__":
    freezer.freeze()
