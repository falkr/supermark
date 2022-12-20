import pypandoc
from packaging import version
from rich import print
from markdown_it import MarkdownIt

from .icons import get_icon


md = MarkdownIt()


def print_pandoc_info():
    installed_pandoc_version = pypandoc.get_pandoc_version()
    print("Installed Pandoc version: {}".format(installed_pandoc_version))
    if version.parse(installed_pandoc_version) < version.parse("2.14"):
        print(
            "There exists a newer version of Pandoc. Update via [link=https://pandoc.org]pandoc.org[/link]."
        )
    # print(pypandoc.get_pandoc_path())
    # print(pypandoc.get_pandoc_formats())


def convert(source: str, target_format: str, source_format: str = "md") -> str:

    if source_format == "md" and target_format == "html":
        result = str(md.render(source))
        if "{{:" in result:
            result = _replace_variables(result)
        return result

    if source_format == "mediawiki":
        extra_args = ["--from", "mediawiki", "--to", "html"]
    else:
        extra_args = []
    return pypandoc.convert_text(
        source, target_format, format=source_format, extra_args=extra_args
    ).strip()


def _replace_variables(input: str) -> str:
    string: str = input
    for variable in ["bi-circle-fill", "bi-circle-half", "bi-circle"]:
        wrapped = "{{:" + variable + ":}}"
        replacement = get_icon(variable.replace("bi-", ""), size="16px")
        if replacement is None or replacement is "":
            replacement = wrapped
            # TODO report missing replacement
            print(f"Replacement not found for variable {variable} {wrapped}")
        string = string.replace(wrapped, replacement)
    return string


def convert_code(source: str, target_format: str) -> str:
    extra_args = ["--highlight-style", "pygments"]
    return pypandoc.convert_text(
        source, target_format, format="md", extra_args=extra_args
    ).strip()
