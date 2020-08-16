import os

import click

from . import __version__
from .build_html import build_html
from .build_latex import build_latex

# @click.version_option(version=__version__)


@click.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
    default=False,
    help="Rebuild all pages, do not regard file timestamps.",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Provide more feedback on what is happening.",
)
@click.option(
    "-d",
    "--draft",
    is_flag=True,
    default=False,
    help="Also print draft parts of the documents.",
)
@click.option(
    "-i",
    "--input",
    "input",
    type=click.Path(exists=True),
    help="Input directory containing the source files.",
)
@click.option(
    "-o", "--output", "output", type=click.Path(exists=True), help="Output directory."
)
@click.option(
    "-t",
    "--template",
    "template",
    type=click.File("rb"),
    help="Template file for the transformation.",
)
# @click.option('-f', '--format', 'html', type=click.Choice(['html', 'pdf'], case_sensitive=False))
def run(all, verbose, draft, input=None, output=None, template=None):
    format = "html"
    input_path = input or os.path.join(os.getcwd(), "pages")
    output_path = output or os.getcwd()
    template_path = template or os.path.join(os.getcwd(), "templates/page.html")
    if format == "pdf":
        build_latex(
            input_path, output_path,
        )
    else:
        build_html(
            input_path,
            output_path,
            template_path,
            rebuild_all_pages=all,
            abort_draft=not draft,
            verbose=verbose,
        )
