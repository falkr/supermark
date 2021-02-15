import os
import random
import re
import string

import pypandoc
import yaml

from .button import Button
from .chunks import HTMLChunk, MarkdownChunk, YAMLDataChunk
from .code import Code
from .figure import Figure
from .hint import Hint
from .hint2 import Hint2
from .lines import Lines
from .parse import ParserState, _parse
from .table import Table
from .video import Video
from .report import Report


def random_id():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=5))


"""
   Chunk  |- HTML
          |- Code
          |- YamlChunk --- YamlDataChunk
          |             |- Table
          |             |- Video
          |             |- Figure
          |             |- Lines
          |             |- Button
          |             |- Lines
          |- Markdown
                |- Hint     
"""


def arrange_assides(chunks):
    main_chunks = []
    current_main_chunk = None
    for chunk in chunks:
        if chunk.is_aside():
            if current_main_chunk is not None:
                current_main_chunk.asides.append(chunk)
            else:
                chunk.raw_chunk.report.tell(
                    "Aside chunk cannot be defined as first element.",
                    level=Report.WARNING,
                )
                main_chunks.append(chunk)
        else:
            main_chunks.append(chunk)
            current_main_chunk = chunk
    return main_chunks
