from enum import Enum


class Report:

    INFO = 1
    WARNING = 2
    ERROR = 3

    def __init__(self, source_path):
        self.source_path = source_path
        self.messages = []
        self.max_level = self.INFO

    def max_level(self):
        return self.max_level

    def tell(self, message, level=1, chunk=None):
        self.max_level = max(self.max_level, level)
        self.messages.append(message)

    def print_(self):
        for m in self.messages:
            print(m)


def print_reports(reports):
    for level in [Report.ERROR, Report.WARNING]:
        for report in reports:
            if report.max_level == level:
                report.print_()
