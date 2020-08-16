import os
from pathlib import Path

import cairosvg
import pypandoc

from .chunks import YAMLChunk
from .report import Report


class Figure(YAMLChunk):
    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(
            raw_chunk,
            dictionary,
            page_variables,
            required=["source"],
            optional=["caption", "link"],
        )
        if dictionary["source"].startswith("http://") or dictionary[
            "source"
        ].startswith("https://"):
            raw_chunk.report.tell(
                "Refer to remote figure: {}".format(dictionary["source"]),
                level=Report.WARNING,
            )
        else:
            self.file_path = os.path.join(
                os.path.dirname(os.path.dirname(raw_chunk.path)), dictionary["source"]
            )
            if not os.path.exists(self.file_path):
                raw_chunk.report.tell(
                    "Figure file {} does not exist.".format(self.file_path),
                    level=Report.WARNING,
                )

    def to_html(self):
        html = []
        html.append('<div class="figure">')
        if "caption" in self.dictionary:
            if "link" in self.dictionary:
                html.append(
                    '<a href="{}"><img src="{}" alt="{}" width="100%"/></a>'.format(
                        self.dictionary["link"],
                        self.dictionary["source"],
                        self.dictionary["caption"],
                    )
                )
            else:
                html.append(
                    '<img src="{}" alt="{}" width="100%"/>'.format(
                        self.dictionary["source"], self.dictionary["caption"]
                    )
                )
            html.append(
                '<span name="{}">&nbsp;</span>'.format(self.dictionary["source"])
            )
            html_caption = pypandoc.convert_text(
                self.dictionary["caption"], "html", format="md"
            )
            html.append(
                '<aside name="{}"><p>{}</p></aside>'.format(
                    self.dictionary["source"], html_caption
                )
            )
        else:
            if "link" in self.dictionary:
                html.append(
                    '<a href="{}"><img src="{}" width="100%"/></a>'.format(
                        self.dictionary["link"], self.dictionary["source"]
                    )
                )
            else:
                html.append(
                    '<img src="{}" width="100%"/>'.format(self.dictionary["source"])
                )
        html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder):
        s = []
        s.append("\\begin{figure}[htbp]")
        # s.append('\\begin{center}')
        # file = '../' + self.dictionary['source']
        figure_file = self.raw_chunk.parent_path / self.dictionary["source"]
        # print(figure_file.suffix)
        if figure_file.suffix == ".gif":
            self.raw_chunk.report.tell(
                "Figure file {} in gif format is not compatible with LaTeX.".format(
                    self.file_path
                ),
                level=Report.WARNING,
            )
            return None
        if figure_file.suffix == ".svg":
            # file = Path(file)
            target_path = self.get_dir_cached() / "{}.pdf".format(figure_file.stem)
            if not target_path.exists():
                # file = self.raw_chunk.parent_path / self.dictionary['source']
                cairosvg.svg2pdf(url=str(figure_file), write_to=str(target_path))
            # s.append('\\includegraphics[width=\\linewidth]{{{}}}%'.format(target_path))
            figure_file = target_path
        figure_file = figure_file.relative_to(builder.output_file.parent)
        # print('figure_file: {}'.format(figure_file))
        s.append("\\includegraphics[width=\\linewidth]{{{}}}%".format(figure_file))
        if "caption" in self.dictionary:
            caption = pypandoc.convert_text(
                self.dictionary["caption"], "latex", format="md"
            ).strip()
            s.append("\\caption{{{}}}".format(caption))
        s.append("\\label{default}")
        # s.append('\\end{center}')
        s.append("\\end{figure}")
        return "\n".join(s)
