import sys

sys.path.insert(0, "../")

from pathlib import Path

from icecream import ic
from supermark import Core, HTMLBuilder, Report

SITES = {
    "TTM4175": "/Users/kraemer/Dropbox/Teaching/TTM4175/website",
    "TTM4175": "/Users/kraemer/Dropbox/Teaching/TTM4115/website",
    "tbl": "/Users/kraemer/Dropbox/Education/TBL Seminar/tbl",
    "science": "/Users/kraemer/Dropbox/Teaching/Design Science/science",
    "tips": "/Users/kraemer/Dropbox/Teaching/tips/thesis-tips",
    "literature": "/Users/kraemer/Dropbox/Teaching/Literature Search/literature",
    "teampy": "/Users/kraemer/Dropbox/Education/TEAMPY/teampy-s/docs",
    "stmpy": "/Users/kraemer/Dropbox/Teaching/TTM4115/STMPY/stmpy/docs",
}


def build_site(name: str, base_path: Path):
    report = Report()
    output_path = Path.cwd() / name
    template_path = base_path / Path("templates/page.html")
    input_path = base_path / "pages"
    core = Core(report=report)
    builder = HTMLBuilder(
        input_path,
        output_path,
        template_path,
        report,
        rebuild_all_pages=True,
        abort_draft=False,
        verbose=False,
        reformat=False,
    )
    builder.set_core(core)
    builder.build()
    report.print(verbose=False)


def test_sites():
    for name, path in SITES.items():
        print(f"Testing {name}")
        build_site(name, Path(path))


# def test_latex():
#     build_file = Path(
#         "/Users/kraemer/Dropbox/Teaching/TTM4115/website 2020/pages/latex.yml"
#     )
#     base_path = build_file.parent.parent
#     build_latex(build_file, base_path)
#     assert True
