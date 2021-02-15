import os

import click
from click import ClickException
from beepy import beep
import pretty_errors

from . import __version__
from .build_html import build_html
from .build_latex import build_latex
from .report import Report

from colorama import init

init(autoreset=True)

# colors = dict(Fore.__dict__.items())
# for color in colors.keys():
#    print(colors[color] + f"{color}")


# @click.version_option(version=__version__)

import time
from watchdog.observers import Observer
from watchdog.events import (
    FileCreatedEvent,
    FileModifiedEvent,
    FileSystemEventHandler,
    LoggingEventHandler,
)


@click.command()
@click.option(
    "-a",
    "--all",
    is_flag=True,
    default=False,
    help="Rebuild all pages, not only modified ones.",
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
    "-c",
    "--continuous",
    is_flag=True,
    default=False,
    help="Observe the source directory and run continuously.",
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
@click.option(
    "-r",
    "--reformat",
    is_flag=True,
    default=False,
    help="Reformat the input file.",
# @click.option('-f', '--format', 'html', type=click.Choice(['html', 'pdf'], case_sensitive=False))
# def runx(all, verbose, draft, continuous, input=None, output=None, template=None):
#    pass


def run(
    all,
    verbose,
    draft,
    continuous,
    input=None,
    output=None,
    template=None,
    reformat=False,
):
    print("Supermark")
    format = "html"
    base_path = input or os.getcwd()
    input_path = os.path.join(base_path, "pages")
    output_path = output or os.getcwd()
    template_path = template or os.path.join(base_path, "templates/page.html")
    print(template_path)
    if continuous:

        class MyHandler(FileSystemEventHandler):
            def on_modified(self, event):
                print(event)
                build_html(
                    input_path,
                    output_path,
                    template_path,
                    rebuild_all_pages=False,
                    abort_draft=not draft,
                    verbose=verbose,
                )

        observer = Observer()
        # event_handler = LoggingEventHandler()
        # observer.schedule(event_handler, input, recursive=True)
        observer.schedule(MyHandler(), input, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        return
    if format == "pdf":
        build_latex(
            input_path,
            output_path,
        )
    else:
        level = build_html(
            input_path,
            output_path,
            template_path,
            rebuild_all_pages=all,
            abort_draft=not draft,
            verbose=verbose,
            reformat=reformat,
        )
        if level == Report.ERROR:
            beep(3)  # sad error
            ex = ClickException("Something is wrong.")
            ex.exit_code = 1
            raise ex
        else:
            beep(5)
