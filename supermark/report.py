from enum import Enum
from .chunks import RawChunk
from colorama import Fore, Back, Style
import indentation

COLOR_1 = Fore.LIGHTBLUE_EX
COLOR_2 = Fore.LIGHTGREEN_EX


class ReportEntry:
    def __init__(self, message: str, level: int, chunk: RawChunk):
        self.message = message
        self.level = level
        self.chunk = chunk
        if chunk:
            self.file = chunk.path
            self.line = chunk.start_line_number
        else:
            self.file, self.line = None, None

    def to_string(self) -> str:
        s = ""
        if self.chunk:
            s = COLOR_1 + str(self.file.name) + " " + COLOR_2 + str(self.line) + "\n"
        if self.level == Report.WARNING:
            s = s + "    "
        elif self.level == Report.ERROR:
            s = s + "    "
        else:
            s = s + "    "
        s = s + Fore.WHITE + indentation.set(self.message, 1)
        return s


class Report:

    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, source_path):
        self.source_path = source_path
        self.messages = []
        self.max_level = self.INFO
        self.files = []

    def max_level(self):
        return self.max_level

    def tell(self, message, level=1, chunk=None):
        self.max_level = max(self.max_level, level)
        entry = ReportEntry(message, level=level, chunk=chunk)
        self.messages.append(entry)
        if entry.file:
            self.files.append(entry.file)

    def print_(self):
        for m in self.messages:
            print(m.to_string())


def print_reports(reports) -> int:
    total_max_level = Report.INFO
    for level in [Report.ERROR, Report.WARNING, Report.INFO]:
        for report in reports:
            if report.max_level == level:
                report.print_()
                if level > total_max_level:
                    total_max_level = level
    return total_max_level
