import pypandoc
from pygments import highlight
from pygments.formatters import LatexFormatter
from pygments.lexers import get_lexer_by_name

from .chunks import Chunk


class Code(Chunk):
    def __init__(self, raw_chunk, page_variables):
        super().__init__(raw_chunk, page_variables)

    def to_html(self):
        extra_args = ["--highlight-style", "pygments"]
        output = pypandoc.convert_text(
            self.get_content(), "html", format="md", extra_args=extra_args
        )
        return output

    def to_latex(self, builder):
        if self.get_first_line().startswith("```"):
            lang = self.get_first_line().replace("```", "").strip()
            code = "".join(self.raw_chunk.lines[1:-1])
        else:
            lang = None
            code = self.get_content()
        lexer = None
        if lang is not None:
            try:
                lexer = get_lexer_by_name(lang, stripall=True)
            except Exception as e:
                pass
        output = []
        if lexer is not None:
            formatter = LatexFormatter(linenos=False, verboptions="breaklines")
            result = highlight(code, lexer, formatter)
            output.append(result)
        else:
            output.append("\\begin{Verbatim}[breaklines]")
            output.append(code)
            output.append("\end{Verbatim}")
        return "\n".join(output)
