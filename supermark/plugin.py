from typing import Dict, List, Optional

from .code import Code
from .parse import RawChunk, ParserState
from .chunks import Chunk, YAMLChunk, MarkdownChunk, HTMLChunk, YAMLDataChunk
import yaml
from .report import Report

POINT_CODE_LANG = "code"
POINT_YAML_TYPE = "yaml"
POINT_PARAGRAPH_CLASS = "paragraph_class"


class Plugin:
    def __init__(self):
        pass


plugins_code_lang: Dict[str, Plugin] = {}
plugins_yaml_type: Dict[str, Plugin] = {}
plugins_paragraph_class: Dict[str, Plugin] = {}


def register_code_lang(lang: str, chunk: Code):
    plugins_code_lang[lang] = chunk


def register_yaml_type(type: str, chunk: YAMLChunk):
    plugins_yaml_type[type] = chunk


def register_paragraph_class(clazz: str, chunk: MarkdownChunk):
    plugins_paragraph_class[clazz] = chunk


def cast(rawchunks: List[RawChunk], report) -> List[Chunk]:
    chunks = []
    page_variables = {}
    for raw in rawchunks:
        chunk = _cast(raw, page_variables, report)
        if chunk is None:
            report.tell(
                "No idea what to do with chunk starting with '{}...'".format(
                    raw.get_first_line()[:10]
                ).replace("\n", ""),
                Report.ERROR,
                raw,
            )
        else:
            chunks.append(chunk)
    return chunks


def _cast_paragraph_class(raw, tag, page_variables, report) -> Optional[MarkdownChunk]:
    if tag in plugins_paragraph_class:
        chunk = plugins_paragraph_class[tag](raw, page_variables)
        return chunk
    else:
        report.tell(
            "Paragraph tag :{}: is unknown.".format(tag),
            level=Report.WARNING,
            chunk=raw,
        )
        return MarkdownChunk(raw, page_variables)


def _cast_yaml(raw, type, dictionary, page_variables) -> Optional[YAMLChunk]:
    if type in plugins_yaml_type:
        chunk = plugins_yaml_type[type](raw, dictionary, page_variables)
        return chunk
    else:
        print("no yanl type: {}".format(type))
    return None


def _cast(raw: RawChunk, page_variables, report) -> Optional[Chunk]:
    chunk_type = raw.get_type()
    if chunk_type == ParserState.MARKDOWN:
        tag = raw.get_tag()
        if tag is None or tag == "aside":
            return MarkdownChunk(raw, page_variables)
        else:
            return _cast_paragraph_class(raw, tag, page_variables, report)
    elif chunk_type == ParserState.YAML:
        dictionary = yaml.safe_load("".join(raw.lines))
        if isinstance(dictionary, dict):
            if "type" in dictionary:
                type = dictionary["type"]
                return _cast_yaml(raw, type, dictionary, page_variables)
            else:
                data_chunk = YAMLDataChunk(raw, dictionary, page_variables)
                try:
                    page_variables.update(data_chunk.dictionary)
                except ValueError as e:
                    print(e)
                return data_chunk
        else:
            raw.tell(
                "Something is wrong with the YAML section.",
                level=Report.ERROR,
            )
    elif chunk_type == ParserState.HTML:
        return HTMLChunk(raw, page_variables)
    elif chunk_type == ParserState.CODE:
        return Code(raw, page_variables)
