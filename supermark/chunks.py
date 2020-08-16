import hashlib

import pypandoc
import yaml

from .parse import ParserState, RawChunk
from .report import Report


class Chunk:
    """ Base class for a chunk.
    """

    def __init__(self, raw_chunk, page_variables):
        self.raw_chunk = raw_chunk
        self.page_variables = page_variables
        self.aside = False
        self.asides = []

    def is_aside(self):
        return self.aside

    def get_asides(self):
        return self.asides

    def get_first_line(self):
        return self.raw_chunk.lines[0]

    def get_last_line(self):
        return self.raw_chunk.lines[-1]

    def get_type(self):
        return self.raw_chunk.type

    def get_start_line_number(self):
        return self.raw_chunk.start_line_number

    def get_content(self):
        return "".join(self.raw_chunk.lines)

    def to_latex(self, builder):
        print("No conversion to latex: " + self.get_content())
        return None

    @staticmethod
    def create_hash(content):
        shake = hashlib.shake_128()
        shake.update(content.encode("utf-8"))
        return shake.hexdigest(3)

    def get_dir_cached(self):
        cached = self.raw_chunk.parent_path / "cached"
        cached.mkdir(parents=True, exist_ok=True)
        return cached


class YAMLChunk(Chunk):
    def __init__(
        self, raw_chunk, dictionary, page_variables, required=None, optional=None
    ):
        super().__init__(raw_chunk, page_variables)
        self.dictionary = dictionary
        required = required or []
        optional = optional or []
        for key in required:
            if key not in self.dictionary:
                raw_chunk.report.tell(
                    "YAML section misses required parameter '{}'.".format(key),
                    level=Report.ERROR,
                    chunk=raw_chunk,
                )
        for key in self.dictionary.keys():
            if (key not in required) and (key not in optional) and (key != "type"):
                raw_chunk.report.tell(
                    "YAML section has unknown parameter '{}'.".format(key),
                    level=Report.WARNING,
                    chunk=raw_chunk,
                )

    def has_post_yaml(self):
        return self.raw_chunk.post_yaml is not None

    def get_post_yaml(self):
        return "".join(self.raw_chunk.post_yaml)


class YAMLDataChunk(YAMLChunk):
    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(raw_chunk, dictionary, page_variables, optional=["status"])

    def to_latex(self, builder):
        return None


class MarkdownChunk(Chunk):
    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)
        self.content = "".join(self.raw_chunk.lines)
        self.is_section = super().get_first_line().startswith("# ")
        if raw_chunk.get_tag() is not None:
            self.class_tag = super().get_first_line().strip().split(":")[1].lower()
            self.aside = self.class_tag == "aside"
            self.content = self.content[len(self.class_tag) + 2 :].strip()
        else:
            self.class_tag = None
            self.aside = False

    def get_content(self):
        return self.content

    def pandoc_to_html(self):
        extra_args = ["--ascii", "--highlight-style", "pygments"]
        extra_args = ["--highlight-style", "pygments"]
        return pypandoc.convert_text(
            self.get_content(), "html", format="md", extra_args=extra_args
        )

    def to_html(self):
        if self.aside:
            aside_id = Chunk.create_hash(self.content)
            output = []
            output.append(
                '<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id)
            )
            output.append(self.pandoc_to_html())
            output.append("</aside>")
            return "".join(output)
        else:
            if self.class_tag:
                output = self.pandoc_to_html()
                output = '<div class="{}">{}</div>'.format(self.class_tag, output)
            else:
                output = self.pandoc_to_html()
            return output

    def wrap(self, content):
        return (
            "\\begin{tcolorbox}[colback=red!5!white,colframe=red!75!black,arc=0pt,outer arc=0pt,leftrule=2pt,rightrule=0pt,toprule=0pt,bottomrule=0pt]"
            + content
            + r"\end{tcolorbox}"
        )

    def bold_prefix(self, prefix):
        return "\\textbf{{{}}} ".format(prefix + ":")

    def markdown_to_latex(self):
        extra_args = ["--ascii", "--highlight-style", "pygments"]
        extra_args = ["--highlight-style", "pygments"]
        content = pypandoc.convert_text(
            self.get_content(), "latex", format="md", extra_args=extra_args
        )
        return content

    def to_latex(self, builder):
        output = self.markdown_to_latex()
        if self.class_tag is None:
            return output
        elif self.class_tag == "aside":
            return self.wrap(output)
        elif self.class_tag == "goals":
            return self.wrap(output)
        elif self.class_tag == "warning":
            return self.wrap(self.bold_prefix("Warning") + output)
        elif self.class_tag == "tip":
            return self.wrap(self.bold_prefix("Tip") + output)
        return output


class HTMLChunk(Chunk):
    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)

    def to_html(self):
        return super().get_content()

    def html_to_latex(self):
        extra_args = ["--ascii", "--highlight-style", "pygments"]
        extra_args = ["--highlight-style", "pygments"]
        return pypandoc.convert_text(
            super().get_content(), "latex", format="html", extra_args=extra_args
        )
        # return None

    def to_latex(self, builder):
        if super().get_content().startswith("<!--"):
            return None
        else:
            print("HTML to Latex:")
            print(super().get_content())
            print()
            print(
                pypandoc.convert_text(super().get_content(), "mediawiki", format="html")
            )
            return self.html_to_latex()
