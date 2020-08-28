import sys

sys.path.insert(0, "../../stmpy")
from pathlib import Path

from supermark.build_html import build_html
from supermark.build_latex import build_latex


def test_html():
    input_path = Path("/Users/kraemer/Dropbox/Teaching/TTM4175/website/pages")
    output_path = Path("/Users/kraemer/Dropbox/Teaching/TTM4175/website")
    template_file = Path(
        "/Users/kraemer/Dropbox/Teaching/TTM4175/website/templates/page.html"
    )
    build_html(input_path, output_path, template_file, rebuild_all_pages=True)
    assert True


def test_latex():
    build_file = Path(
        "/Users/kraemer/Dropbox/Teaching/TTM4115/website 2020/pages/latex.yml"
    )
    base_path = build_file.parent.parent
    build_latex(build_file, base_path)
    assert True
