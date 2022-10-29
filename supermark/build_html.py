from concurrent.futures import ThreadPoolExecutor, Future
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set, Optional
import yaml
from yaml.scanner import ScannerError
from rich.progress import Progress, BarColumn


from .chunks import Builder, Chunk, MarkdownChunk, YAMLDataChunk
from .report import Report
from .utils import write_file, add_notnone


def reverse_path(parent_path: Path, child_path: Path) -> str:
    levels = len(child_path.relative_to(parent_path).parent.parts)
    s = ""
    for _ in range(levels):
        s = "../" + s
    return s


class Page:
    def __init__(self, d: Dict[str, str], children: Optional[List["Page"]] = None):
        self.page = d["page"]
        self.title = d["title"] if "title" in d else d["page"]
        # TODO handle that these are not set
        self.children = children
        self.parent = None
        if self.children:
            for child in self.children:
                child.parent = self

    def __str__(self):
        return self.title


class Breadcrumbs:
    def __init__(self, report: Report):
        self.pages: Dict[str, Page] = {}
        self.report = report

    def load(self, path: Path):
        with open(path) as f:
            try:
                temp: Any = yaml.safe_load(f)
                self.roots = self.parse_breadcrumbs(temp)
            except ScannerError as e:
                self.report.warning(str(e), path)

    def parse_breadcrumbs(self, l: List[Any]) -> List[Any]:
        tchildren = []
        for i in range(len(l)):
            item = l[i]
            if isinstance(item, dict):
                if i < len(l) - 1 and isinstance(l[i + 1], list):
                    children = self.parse_breadcrumbs(l[i + 1])
                else:
                    children = None
                page = Page(item, children=children)
                tchildren.append(page)
                self.pages[page.page] = page
        return tchildren

    def has_breadcrumbs(self, page: str) -> bool:
        return page in self.pages

    def get_trail(self, page: str) -> List[Page]:
        trail: List[Page] = []
        while page in self.pages:
            p = self.pages[page]
            trail.append(p)
            if p.parent:
                page = p.parent.page
            else:
                break
        trail.reverse()
        return trail

    def get_html(self, page_name: str) -> str:
        html: List[str] = []
        divider = "url(&#34;data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8'%3E%3Cpath d='M2.5 0L1 1.5 3.5 4 1 6.5 2.5 8l4-4-4-4z' fill='%236c757d'/%3E%3C/svg%3E&#34;)"
        html.append(
            f'<nav style="--bs-breadcrumb-divider: {divider};" aria-label="breadcrumb">'
        )
        html.append('<ol class="breadcrumb">')
        for page in self.get_trail(page_name):
            if page.page == page_name:
                html.append(
                    f'<li class="breadcrumb-item active" aria-current="page">{page.title}</li>'
                )
            else:
                html.append(
                    f'<li class="breadcrumb-item"><a href="{page.page.replace(".md", ".html")}">{page.title}</a></li>'
                )
        html.append("</ol>")
        html.append("</nav>")
        return "\n".join(html)


class HTMLBuilder(Builder):
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        template_file: Path,
        report: Report,
        rebuild_all_pages: bool = True,
        abort_draft: bool = True,
        verbose: bool = False,
        reformat: bool = False,
    ) -> None:
        super().__init__(
            input_path,
            output_path,
            template_file,
            report,
            rebuild_all_pages,
            abort_draft,
            verbose,
            reformat,
        )
        breadcrumbs_path = input_path / Path("breadcrumbs.yaml")
        self.breadcrumbs = Breadcrumbs(self.report)
        self.report.info(f"Looking for breadcrumbs file in {breadcrumbs_path}")
        if breadcrumbs_path.exists():
            self.report.info(f"Breadcrumbs exist in {breadcrumbs_path}")
            self.breadcrumbs.load(breadcrumbs_path)

    def _transform_page_to_html(
        self,
        chunks: Sequence[Chunk],
        template: str,
        source_file_path: Path,
        report: Report,
        css: str,
        js: str,
    ) -> str:
        content: Sequence[str] = []
        content.append('<div class="page">')
        if len(chunks) == 0:
            pass
        else:
            first_chunk = chunks[0]
            if isinstance(first_chunk, MarkdownChunk) and not first_chunk.is_section:
                content.append('    <section class="content">')

        page_path = str(source_file_path.relative_to(self.input_path))
        if self.breadcrumbs.has_breadcrumbs(page_path):
            content.append(self.breadcrumbs.get_html(page_path))

        for chunk in chunks:
            if (
                "status" in chunk.page_variables
                and self.abort_draft
                and chunk.page_variables["status"] == "draft"
            ):
                content.append("<mark>This site is under construction.</mark>")
                break
            if isinstance(chunk, YAMLDataChunk):
                pass
            elif not chunk.is_ok():
                print("chunk not ok")
                pass
            elif isinstance(chunk, MarkdownChunk):
                if chunk.is_section:
                    # open a new section
                    content.append("    </section>")
                    content.append('    <section class="content">')
                # TODO maybe we want to put the anchor element to the top?
                for aside in chunk.asides:
                    add_notnone(aside.to_html(self), content)
                add_notnone(chunk.to_html(self), content)
            else:
                add_notnone(chunk.to_html(self), content)
                for aside in chunk.asides:
                    add_notnone(aside.to_html(self), content)

        content.append("    </section>")
        content.append("</div>")
        content = "\n".join(content)
        for tag in ["content", "css", "js", "rel_path"]:
            if "{" + tag + "}" not in template:
                self.report.warning(
                    "The template does not contain insertion tag {" + tag + "}"
                )
        # Can throw KeyError, if the template contains keys like { css } and not {css}

        try:
            return template.format_map(
                {
                    "content": content,
                    "css": css,
                    "js": js,
                    "rel_path": reverse_path(self.input_path, source_file_path),
                }
            )
        except KeyError as e:
            report.error(f"The template contains an unknown key {str(e)}")
            return ""

    def _create_target(
        self,
        source_file_path: Path,
        target_file_path: Path,
        template_file_path: Path,
        overwrite: bool,
    ) -> bool:
        if not target_file_path.is_file():
            return True
        if overwrite:
            return True
        if not template_file_path.is_file():
            return target_file_path.stat().st_mtime < source_file_path.stat().st_mtime
        else:
            return (
                target_file_path.stat().st_mtime < source_file_path.stat().st_mtime
            ) or (target_file_path.stat().st_mtime < template_file_path.stat().st_mtime)

    def _process_file(
        self,
        source_file_path: Path,
        target_file_path: Path,
        template: str,
    ):

        extensions_used: Set[Extension] = set()
        chunks = self.parse_file(source_file_path, extensions_used)
        if not chunks:
            # TODO warn that the page is empty, and therefore nothing is written
            return
        html = self._transform_page_to_html(
            chunks,
            template,
            source_file_path,
            self.report,
            self.core.get_css(self.extensions_used),
            self.core.get_js(self.extensions_used),
        )
        write_file(html, target_file_path, self.report)
        self.report.info("Translated", path=target_file_path)

    def _default_html_template(self) -> str:
        html: Sequence[str] = []
        html.append('<head><title></title><style type="text/css">{css}</style></head>')
        html.append("<body>")
        html.append("{content}")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)

    def _load_html_template(self, template_path: Path, report: Report) -> str:
        try:
            with open(
                template_path, "r", encoding="utf-8", errors="surrogateescape"
            ) as templatefile:
                template = templatefile.read()
                self.report.info("Loading template {}.".format(template_path))
                return template
        except FileNotFoundError:
            self.report.warning(
                "Template file missing. Expected at {}. Using default template.".format(
                    template_path
                )
            )
            return self._default_html_template()

    def build(
        self,
    ) -> None:
        template = self._load_html_template(self.template_file, self.report)
        jobs: Sequence[Dict[str, Any]] = []
        files = list(
            self.input_path.glob(
                "**/*.md",
            )
        )
        self.output_path.mkdir(exist_ok=True, parents=True)
        for source_file_path in files:
            target_file_path: Path = (
                self.output_path
                / source_file_path.relative_to(self.input_path).parent
                / (source_file_path.stem + ".html")
            )
            if self._create_target(
                source_file_path,
                target_file_path,
                self.template_file,
                self.rebuild_all_pages,
            ):
                target_file_path.parent.mkdir(exist_ok=True, parents=True)
                jobs.append(
                    {
                        "source_file_path": source_file_path,
                        "target_file_path": target_file_path,
                        "template": template,
                        "abort_draft": self.abort_draft,
                    }
                )
        if len(files) == 0:
            self.report.conclude(
                "No source files (*.md) detected. Searched in {}".format(
                    self.input_path
                )
            )
            return
        elif len(jobs) == 0:
            self.report.conclude(
                "No changed files detected. To re-build all unchanged files, use the [bold]--all[/bold] option."
            )
            return
        if len(jobs) == 1:
            self.report.info("Using single thread.")
            with Progress(transient=True) as progress:
                progress.add_task("[orange]Building 1 page", start=False)
                self._process_file(
                    jobs[0]["source_file_path"],
                    jobs[0]["target_file_path"],
                    jobs[0]["template"],
                )
        else:
            with ThreadPoolExecutor() as e:
                self.report.info("Using threadpool.")
                with Progress(
                    "[progress.description]{task.description}",
                    BarColumn(),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    transient=True,
                ) as progress:
                    task = progress.add_task(
                        f"[orange]Building {len(jobs)} pages",
                        total=len(jobs),
                    )
                    futures = []
                    for job in jobs:
                        future = e.submit(
                            self._process_file,
                            job["source_file_path"],
                            job["target_file_path"],
                            job["template"],
                        )
                        future.add_done_callback(
                            lambda p: progress.update(task, advance=1.0)
                        )
                        futures.append(future)
                    for future in futures:
                        future.result()


# from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer
# def build_html_continuously(
#     self,
#     input_path: Path,
#     output_path: Path,
#     template_path: Path,
#     draft: bool,
#     verbose: bool,
# ):
#     class MyHandler(FileSystemEventHandler):
#         def on_modified(self, event):
#             print(event)
#             self.build()

#     observer = Observer()
#     # event_handler = LoggingEventHandler()
#     # observer.schedule(event_handler, input, recursive=True)
#     observer.schedule(MyHandler(), input, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(10)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
