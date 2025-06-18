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

def test_pages_have_html_extension():
    expected_pages = [
        "contact/index.html",
        "coulisses/index.html",
        "rh-chatbot/index.html",
        "test-zone/index.html",
        "test/index.html",
    ]
    for page in expected_pages:
        assert os.path.exists(os.path.join("build", page)), f"Missing {page}"

def test_no_raw_markdown():
    html_files = glob.glob("build/**/*.html", recursive=True)
    md_pattern = re.compile(r"^#|```", re.MULTILINE)
    for path in html_files:
        data = codecs.open(path, "r", "utf-8").read()
        assert not md_pattern.search(data), f"Raw markdown found in {path}"
