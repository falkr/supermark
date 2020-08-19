import re
from enum import Enum
from pathlib import Path


class ParserState(Enum):
    MARKDOWN = 0
    YAML = 1
    CODE = 2
    HTML = 3
    AFTER_YAML = 4
    AFTER_YAML_CONTENT = 5


ENV_PATTERN = re.compile("[a-zA-Z]*:")


def is_empty(s_line):
    return not s_line


class RawChunk:
    def __init__(self, lines, chunk_type, start_line_number, path, report):
        self.lines = lines
        self.type = chunk_type
        self.start_line_number = start_line_number
        self.path = path
        self.parent_path = Path(path).parent.parent
        self.report = report
        # check if we only got empty lines
        def all_empty(lines):
            if len(lines) == 0:
                return True
            for line in lines:
                if line.strip():
                    return False
            return True

        self._is_empty = all_empty(self.lines)
        # remove blank lines from the beginning
        while len(self.lines) > 0 and is_empty(self.lines[0].strip()):
            self.lines.pop(0)
            self.start_line_number = self.start_line_number + 1
        self.tag = None
        if len(self.lines) > 0:
            if has_class_tag(self.lines[0]):
                self.tag = self.lines[0].strip().split(":")[1].lower()
        self.post_yaml = None

    def get_tag(self):
        return self.tag

    def is_empty(self):
        return self._is_empty

    def get_type(self):
        return self.type

    def get_first_line(self):
        if len(self.lines) == 0:
            return "empty"
        return self.lines[0]


def yaml_start(s_line):
    return s_line == "---"


def yaml_stop(s_line):
    return s_line == "---"


def has_class_tag(s_line):
    return s_line.startswith(":") and ENV_PATTERN.match(s_line)


def markdown_start(s_line, empty_lines):
    return (
        has_class_tag(s_line)
        or s_line.startswith("# ")
        or empty_lines >= 2
        or s_line.startswith("Aside:")
    )


def html_start(s_line, empty_lines):
    return s_line.startswith("<") and empty_lines >= 2


def html_stop(empty_lines):
    return empty_lines >= 2


def code_start(s_line):
    return s_line.startswith("```")


def code_stop(s_line):
    return s_line.startswith("```")


def _parse(lines, path, report):
    chunks = []
    current_lines = []
    empty_lines = 0
    state = ParserState.MARKDOWN
    start_line_number = 0
    previous_yaml_chunk = None

    for line_number, line in enumerate(lines, start=1):
        s_line = line.strip()
        if state == ParserState.MARKDOWN:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif yaml_start(s_line):
                chunks.append(
                    RawChunk(
                        current_lines,
                        ParserState.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.YAML
                current_lines = []
                start_line_number = line_number
                empty_lines = 0
            elif code_start(s_line):
                chunks.append(
                    RawChunk(
                        current_lines,
                        ParserState.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.CODE
                current_lines = [line]
                start_line_number = line_number
                empty_lines = 0
            elif html_start(s_line, empty_lines):
                chunks.append(
                    RawChunk(
                        current_lines,
                        ParserState.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.HTML
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            elif markdown_start(s_line, empty_lines):
                chunks.append(
                    RawChunk(
                        current_lines,
                        ParserState.MARKDOWN,
                        start_line_number,
                        path,
                        report,
                    )
                )
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
        elif state == ParserState.YAML:
            if yaml_stop(s_line):
                previous_yaml_chunk = RawChunk(
                    current_lines, ParserState.YAML, start_line_number, path, report
                )
                chunks.append(previous_yaml_chunk)
                state = ParserState.AFTER_YAML
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state == ParserState.AFTER_YAML:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
                state = ParserState.MARKDOWN
                previous_yaml_chunk = None
            else:
                current_lines.append(line)
                state = ParserState.AFTER_YAML_CONTENT
                empty_lines = 0
        elif state == ParserState.AFTER_YAML_CONTENT:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                if empty_lines > 1:
                    previous_yaml_chunk.post_yaml = current_lines
                    state = ParserState.MARKDOWN
                    current_lines = []
                else:
                    current_lines.append(line)
                start_line_number = line_number + 1
            else:
                empty_lines = 0
                current_lines.append(line)
        elif state == ParserState.CODE:
            if code_stop(s_line):
                current_lines.append(line)
                chunks.append(
                    RawChunk(
                        current_lines, ParserState.CODE, start_line_number, path, report
                    )
                )
                state = ParserState.MARKDOWN
                current_lines = []
                start_line_number = line_number + 1
            else:
                current_lines.append(line)
        elif state == ParserState.HTML:
            if is_empty(s_line):
                empty_lines = empty_lines + 1
                current_lines.append(line)
            elif html_stop(empty_lines):
                chunks.append(
                    RawChunk(
                        current_lines, ParserState.HTML, start_line_number, path, report
                    )
                )
                state = ParserState.MARKDOWN
                current_lines = []
                current_lines.append(line)
                start_line_number = line_number
                empty_lines = 0
            else:
                current_lines.append(line)
                empty_lines = 0
    # create last chunk
    chunks.append(RawChunk(current_lines, state, start_line_number, path, report))
    # remove chunks that turn out to be empty
    chunks = [item for item in chunks if not item.is_empty()]
    return chunks
