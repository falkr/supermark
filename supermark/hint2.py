import os
import re

import pypandoc

from .chunks import YAMLChunk
from .report import Report


class Hint2(YAMLChunk):
    def __init__(self, raw_chunk, dictionary, page_variables):
        super().__init__(
            raw_chunk, dictionary, page_variables, required=[], optional=["title"],
        )
        self.title = dictionary["title"] if "title" in dictionary else ""
        if self.has_post_yaml():
            self.hint = self.get_post_yaml()
        else:
            raw_chunk.report.tell(
                "Hint should have a post-yaml section with the content.", Report.WARNING
            )
            self.hint = ""

    def to_html(self):
        html = []
        html.append('<button class="w3collapsible">{}</button>'.format(self.title))
        html.append('<div class="w3content">')
        content = pypandoc.convert_text(self.hint, "html", format="md")
        html.append(content)
        html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder):
        latex = []
        # TODO
        return "\n".join(latex)
