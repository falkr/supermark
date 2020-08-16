import os
import re

import pypandoc
import wikitextparser as wtp

from .chunks import YAMLChunk
from .report import Report


class Table(YAMLChunk):
    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(
            raw_chunk,
            dictionary,
            page_variables,
            required=[],
            optional=["file", "class", "caption"],
        )
        self.div_class = None if "class" not in dictionary else dictionary["class"]
        if self.has_post_yaml():
            self.table_raw = self.get_post_yaml()
        else:
            file_path = os.path.join(
                os.path.dirname(os.path.dirname(raw_chunk.path)), dictionary["file"]
            )
            if not os.path.exists(file_path):
                raw_chunk.report.tell(
                    "Table file {} does not exist.".format(file_path),
                    level=Report.ERROR,
                )
                # TODO somehow mark this chunk and do not try to generate HTML or Latex from it
            else:
                with open(file_path, "r") as myfile:
                    self.table_raw = myfile.read()

    def to_html(self):
        html = []
        extra_args = ["--from", "mediawiki", "--to", "html"]
        output = pypandoc.convert_text(
            self.table_raw, "html", format="md", extra_args=extra_args
        )
        if self.div_class:
            output = re.sub(
                "(<table)(>)", '\\1 class="{}"\\2'.format(self.div_class), output
            )
        html.append(output)
        if "caption" in self.dictionary:
            html.append('<span name="{}">&nbsp;</span>'.format(self.dictionary["file"]))
            html_caption = pypandoc.convert_text(
                self.dictionary["caption"], "html", format="md"
            )
            html.append(
                '<aside name="{}"><p>{}</p></aside>'.format(
                    self.dictionary["file"], html_caption
                )
            )
        return "\n".join(html)

    def get_scss(self):
        return """section {
                    border:1px solid #e5e5e5;
                    border-width:1px 0;
                    padding:20px 0;
                    margin:0 0 20px;
                  }"""

    def to_latex(self, builder):
        parsed = wtp.parse(self.table_raw)
        # print(parsed)
        rows = parsed.tables[0].data()
        rowspec = ""
        # print(rows[0])
        # print(type(rows[0]))
        for _ in rows[0]:
            rowspec = rowspec + "L"
        # https://pypi.org/project/wikitextparser/#tables
        latex = []
        latex.append("\\begin{table*}[t]")
        latex.append("\\begin{tabulary}{\\textwidth}" + "{{{}}}".format(rowspec))
        latex.append("\\toprule")
        for row in rows:
            resolved_row = []
            for x in row:
                resolved_row.append(
                    pypandoc.convert_text(x, "latex", format="mediawiki")
                )
            latex.append("&".join(resolved_row) + "\\\\")
        latex.append("\\bottomrule")
        latex.append("\\end{tabulary}")
        if "caption" in self.dictionary:
            caption = pypandoc.convert_text(
                self.dictionary["caption"], "latex", format="md"
            )
            latex.append("\\caption{{{}}}".format(caption))
        if "label" in self.dictionary:
            latex.append("\\label{{{}}}".format(self.dictionary["label"]))
        latex.append("\\end{table*}")
        # extra_args = ['--from', 'mediawiki', '--to', 'latex']
        # output = pypandoc.convert_text(self.table_raw, 'latex', format='md', extra_args=extra_args)
        return "\n".join(latex)
