import os
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm
import blindspin

from .chunks import MarkdownChunk, YAMLDataChunk
from .core import arrange_assides
from .parse import _parse
from .report import Report, print_reports
from .plugin import cast


def transform_page_to_html(lines, template, filepath, abort_draft, report):
    chunks = _parse(lines, filepath, report)
    chunks = cast(chunks, report)
    chunks = arrange_assides(chunks)

    content = []
    content.append('<div class="page">')
    if len(chunks) == 0:
        pass
    else:
        first_chunk = chunks[0]
        if isinstance(first_chunk, MarkdownChunk) and not first_chunk.is_section:
            content.append('    <section class="content">')

    for chunk in chunks:
        if (
            "status" in chunk.page_variables
            and abort_draft
            and chunk.page_variables["status"] == "draft"
        ):
            content.append("<mark>This site is under construction.</mark>")
            break
        if isinstance(chunk, YAMLDataChunk):
            pass
        elif not chunk.is_ok():
            pass
        elif isinstance(chunk, MarkdownChunk):
            if chunk.is_section:
                # open a new section
                content.append("    </section>")
                content.append('    <section class="content">')
            # TODO maybe we want to put the anchor element to the top?
            for aside in chunk.asides:
                content.append(aside.to_html())
            content.append(chunk.to_html())
        else:
            content.append(chunk.to_html())
            for aside in chunk.asides:
                content.append(aside.to_html())

    content.append("    </section>")
    content.append("</div>")
    content = "\n".join(content)
    parameters = {"content": content}
    html = template.format(**parameters)
    return html


def _create_target(source_file_path, target_file_path, template_file_path, overwrite):
    if not os.path.isfile(target_file_path):
        return True
    if overwrite:
        return True
    if not os.path.isfile(template_file_path):
        return os.path.getmtime(target_file_path) < os.path.getmtime(source_file_path)
    else:
        return os.path.getmtime(target_file_path) < os.path.getmtime(
            source_file_path
        ) or os.path.getmtime(target_file_path) < os.path.getmtime(template_file_path)


def write_file(html, target_file_path, report):
    encoding = "utf-8"
    try:
        with open(target_file_path, "w", encoding=encoding) as html_file:
            html_file.write(html)
    except UnicodeEncodeError as error:
        report.tell(
            "Encoding error when writing file {}.".format(target_file_path),
            level=Report.ERROR,
        )
        character = error.object[error.start : error.end]
        line = html.count("\n", 0, error.start) + 1
        report.tell(
            "Character {} in line {} cannot be saved with encoding {}.".format(
                character, line, encoding
            ),
            level=Report.ERROR,
        )
        with open(
            target_file_path, "w", encoding=encoding, errors="ignore"
        ) as html_file:
            html_file.write(html)


def remove_empty_lines_begin_and_end(code):
    lines = code.splitlines()
    start = 0
    for i, line in enumerate(lines):
        if line.strip():
            start = i
            break
    end = len(lines)
    for i, line in enumerate(lines[::-1]):
        if line.strip():
            end = len(lines) - i
            break
    return "\n".join(lines[start:end])


def process_file(source_file_path, target_file_path, template, abort_draft, reformat):
    with open(source_file_path, "r", encoding="utf-8") as file:
        report = Report(source_file_path)
        lines = file.readlines()
        # report.tell("{}".format(source_file_path), Report.INFO)
        html = transform_page_to_html(
            lines, template, source_file_path, abort_draft, report
        )
        write_file(html, target_file_path, report)

        if reformat:
            chunks = _parse(lines, source_file_path, report)
            chunks = cast(chunks, report)
            source_code = ""
            for chunk in chunks:
                code = chunk.recode()
                if code is not None:
                    source_code = source_code + remove_empty_lines_begin_and_end(code)
                    source_code = source_code + "\n\n"
            write_file(source_code, source_file_path, report)

        return report


def default_html_template():
    html = []
    html.append("<head><title></title></head>")
    html.append("<body>")
    html.append("{content}")
    html.append("</body>")
    html.append("</html>")
    return "\n".join(html)


def load_html_template(template_path, report):
    try:
        with open(
            template_path, "r", encoding="utf-8", errors="surrogateescape"
        ) as templatefile:
            template = templatefile.read()
            report.tell("Loading template {}.".format(template_path), Report.INFO)
            return template
    except FileNotFoundError:
        report.tell(
            "Template file missing. Expected at {}. Using default template.".format(
                template_path
            ),
            Report.WARNING,
        )
        return default_html_template()


def build_html(
    input_path,
    output_path,
    template_file,
    rebuild_all_pages=True,
    abort_draft=True,
    verbose=False,
    reformat=False,
):
    reports = []
    report = Report(None)
    template = load_html_template(template_file, report)
    jobs = []
    with blindspin.spinner():
        for filename in os.listdir(input_path):
            source_file_path = os.path.join(input_path, filename)
            if os.path.isfile(source_file_path) and filename.endswith(".md"):
                target_file_name = (
                    os.path.splitext(os.path.basename(filename))[0] + ".html"
                )
                target_file_path = os.path.join(output_path, target_file_name)
                if _create_target(
                    source_file_path, target_file_path, template_file, rebuild_all_pages
                ):
                    jobs.append(
                        {
                            "source_file_path": source_file_path,
                            "target_file_path": target_file_path,
                            "template": template,
                            "abort_draft": abort_draft,
                        }
                    )
    if len(jobs) == 0:
        print(
            "No changed files detected. To translate all files, use the --all option."
        )
        return
    if len(jobs) == 1:
        with blindspin.spinner():
            process_file(
                jobs[0]["source_file_path"],
                jobs[0]["target_file_path"],
                jobs[0]["template"],
                jobs[0]["abort_draft"],
                reformat,
            )
    else:
        with ThreadPoolExecutor() as e:
            with tqdm(total=len(jobs)) as progress:
                futures = []
                for job in jobs:
                    future = e.submit(
                        process_file,
                        job["source_file_path"],
                        job["target_file_path"],
                        job["template"],
                        job["abort_draft"],
                        reformat,
                    )
                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)
                for future in futures:
                    reports.append(future.result())
    return print_reports(reports)
