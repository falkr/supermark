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


def cast(rawchunks):
    chunks = []
    page_variables = {}
    for raw in rawchunks:
        chunk_type = raw.get_type()
        if chunk_type == ParserState.MARKDOWN:
            if raw.get_tag() == "hint":
                chunks.append(Hint(raw, page_variables))
            else:
                chunks.append(MarkdownChunk(raw, page_variables))
        elif chunk_type == ParserState.YAML:
            dictionary = yaml.safe_load("".join(raw.lines))
            if isinstance(dictionary, dict):
                if "type" in dictionary:
                    yaml_type = dictionary["type"]
                    if yaml_type == "youtube":
                        chunks.append(Video(raw, dictionary, page_variables))
                    elif yaml_type == "figure":
                        chunks.append(Figure(raw, dictionary, page_variables))
                    elif yaml_type == "button":
                        chunks.append(Button(raw, dictionary, page_variables))
                    elif yaml_type == "lines":
                        chunks.append(Lines(raw, dictionary, page_variables))
                    elif yaml_type == "table":
                        chunks.append(Table(raw, dictionary, page_variables))
                    elif yaml_type == "hint":
                        chunks.append(Hint2(raw, dictionary, page_variables))
                    # TODO warn if unknown type
                else:
                    data_chunk = YAMLDataChunk(raw, dictionary, page_variables)
                    try:
                        page_variables.update(data_chunk.dictionary)
                    except ValueError as e:
                        print(e)
                    chunks.append(data_chunk)
            else:
                raw.report.tell(
                    "Something is wrong with the YAML section.",
                    level=Report.ERROR,
                    chunk=raw,
                )
        elif chunk_type == ParserState.HTML:
            chunks.append(HTMLChunk(raw, page_variables))
        elif chunk_type == ParserState.CODE:
            chunks.append(Code(raw, page_variables))
    return chunks


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
