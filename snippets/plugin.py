from typing import Dict, List, Optional
from pathlib import Path
from icecream import ic

from .code import Code
from .parse import RawChunk, ParserState
from .chunks import Chunk, YAMLChunk, MarkdownChunk, HTMLChunk, YAMLDataChunk
import yaml
from .report import Report

POINT_CODE_LANG = "code"
POINT_YAML_TYPE = "yaml"
POINT_PARAGRAPH_CLASS = "paragraph_class"

plugins = {}


def get_plugins():
    return plugins.values()


def get_plugin(name: str):
    return plugins[name]


class Plugin:
    def __init__(self, source_file: str):
        self.chunk = None
        self.source_file = source_file
        ic(self.source_file)
        self.dir = Path(self.source_file).parent

    def find_files(self, pattern: str):
        return list(self.dir.glob(pattern))

    def get_css(self):
        return self.find_files("*.css")

    def get_examples(self):
        return self.find_files("examples/*.md")


class YAMLPlugin(Plugin):
    def __init__(self, source_file: str):
        super().__init__(source_file=source_file)


class MarkdownParagraphPlugin(Plugin):
    def __init__(self, type, source_file: str = __file__):
        super().__init__(source_file=source_file)
        self.type = type


class CodeLangPlugin(Plugin):
    def __init__(self, source_file: str):
        super().__init__(source_file=source_file)


class TablePlugin(Plugin):
    # css of table class
    # if cells should be empty or filled with &nbsp;
    def __init__(self, source_file: str):
        super().__init__(source_file=source_file)


plugins_code_lang: Dict[str, Plugin] = {}
plugins_yaml_type: Dict[str, Plugin] = {}
plugins_paragraph_class: Dict[str, Plugin] = {}
plugins_tables: Dict[str, Plugin] = {}


def register_code_lang(lang: str, chunk: Code, plugin: Plugin):
    plugins[lang] = plugin
    plugins_code_lang[lang] = plugin
    plugin.chunk_class = chunk


def register_yaml_type(type: str, chunk: YAMLChunk, plugin: Plugin):
    plugins[type] = plugin
    plugins_yaml_type[type] = plugin
    plugin.chunk_class = chunk


def register_paragraph_class(clazz: str, chunk: MarkdownChunk, plugin: Plugin):
    plugins[clazz] = plugin
    plugins_paragraph_class[clazz] = plugin
    plugin.chunk_class = chunk


# tables are a different plugin, they have a YAMLChunk as base, dont specify an own chunk
def register_table(clazz: str, chunk: YAMLChunk, plugin: Plugin):
    plugins[clazz] = plugin
    plugins_tables[clazz] = plugin
    plugin.chunk_class = chunk


def cast(rawchunks: List[RawChunk], report: Report) -> List[Chunk]:
    chunks = []
    page_variables = {}
    for raw in rawchunks:
        chunk = _cast(raw, page_variables, report)
        if chunk is None:
            report.tell(
                "No ideas what to do with chunk starting with '{}...'".format(
                    raw.get_first_line()[:10]
                ).replace("\n", ""),
                Report.ERROR,
                raw,
            )
        else:
            chunks.append(chunk)
    return chunks


def _cast_paragraph_class(
    raw, tag, page_variables, report: Report
) -> Optional[MarkdownChunk]:
    if tag in plugins_paragraph_class:
        chunk = plugins_paragraph_class[tag].chunk_class(raw, page_variables)
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
        chunk = plugins_yaml_type[type].chunk_class(raw, dictionary, page_variables)
        return chunk
    else:
        print("no yaml type: {}".format(type))
    return None


def _cast(raw: RawChunk, page_variables, report: Report) -> Optional[Chunk]:
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
