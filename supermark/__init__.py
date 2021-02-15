from .build_html import build_html
from .build_latex import build_latex
from .chunks import Chunk, HTMLChunk, MarkdownChunk, YAMLChunk, YAMLDataChunk
from .parse import RawChunk
from .plugin import register_code_lang, register_paragraph_class, register_yaml_type
from .button import Button
from .chunks import HTMLChunk, MarkdownChunk, YAMLDataChunk
from .code import Code
from .figure import Figure
from .hint import Hint
from .hint2 import Hint2
from .lines import Lines
from .table import Table
from .video import Video

__version__ = "0.2.3"

__all__ = [
    "RawChunk",
    "Chunk",
    "YAMLChunk",
    "YAMLDataChunk",
    "MarkdownChunk",
    "HTMLChunk",
    "build_html",
    "build_latex",
    "build_latex_yaml",
]

register_yaml_type('figure', Figure)
register_yaml_type('button', Button)
register_yaml_type('hint', Hint2)
register_yaml_type('lines', Lines)
register_yaml_type('table', Table)
register_yaml_type('video', Video)
register_yaml_type('youtube', Video)

register_paragraph_class("goals", MarkdownChunk)
register_paragraph_class("todo", MarkdownChunk)
register_paragraph_class("steps", MarkdownChunk)
register_paragraph_class("tip", MarkdownChunk)
register_paragraph_class("tips", MarkdownChunk)
register_paragraph_class("warning", MarkdownChunk)
register_paragraph_class("hint", MarkdownChunk)
register_paragraph_class("rat", MarkdownChunk)