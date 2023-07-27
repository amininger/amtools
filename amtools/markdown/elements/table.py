from typing import List

from .markdown_element import MarkdownElement
from .inline_text import InlineText

class Table(MarkdownElement):
    def __init__(self, headings: List[InlineText]):
        self.headings = headings
        self.num_cols = len(self.headings)
        self.rows = []
        self.widths = [ self.calc_width(h.raw_text()) for h in self.headings ]

    def calc_width(self, text):
        return 5 + max(len(s) for s in text.split("<br>"))

    def children(self):
        children = list(self.headings)
        for row in self.rows:
            children += row
        return children

    def add_row(self, row: List[InlineText]) -> None:
        new_row = []
        for i in range(self.num_cols):
            if i < len(row):
                new_row.append(row[i])
            else:
                new_row.append(InlineText())
            self.widths[i] = max(self.widths[i], self.calc_width(new_row[i].raw_text()))
        self.rows.append(new_row)

    def print_headings(self) -> str:
        return "| " + " | ".join(self.headings[i].raw_text().center(w) for i, w in enumerate(self.widths)) + " |"

    def print_hline(self) -> str:
        return "+" + "+".join( "-"*(w+2) for w in self.widths) + "+"

    def print_row(self, row) -> str:
        return "| " + " | ".join(row[i].raw_text().ljust(w) for i, w in enumerate(self.widths)) + " |"

    def __str__(self) -> str:
        lines = []
        lines.append(self.print_hline())
        lines.append(self.print_headings())
        lines.append(self.print_hline())
        for row in self.rows:
            lines.append(self.print_row(row))
        lines.append(self.print_hline())

        return "\n".join(lines)

