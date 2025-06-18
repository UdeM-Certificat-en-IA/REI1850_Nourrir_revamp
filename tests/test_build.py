import glob
import os
import re
import codecs

def test_index_exists():
    assert os.path.exists("build/index.html")

def test_no_jinja_left():
    html_files = glob.glob("build/**/*.html", recursive=True)
    tag = re.compile(r"{{|{%")
    for path in html_files:
        data = codecs.open(path, "r", "utf-8").read()
        assert not tag.search(data), f"Jinja tag left in {path}"
