from enum import Enum
from typing import List

from .markdown_element import MarkdownElement
from .inline_text import InlineText

class TaskItemStatus(Enum):
    """ The possible statuses of a TaskItem """
    INCOMPLETE = 1
    COMPLETE   = 2
    UNKNOWN    = 3

class TaskItem(MarkdownElement):
    """ A specific task item to complete """
    def __init__(self, text: InlineText, status: TaskItemStatus):
        self.text = text
        self.status = status

    def symbol(self):
        if self.status == TaskItemStatus.INCOMPLETE: return ' '
        if self.status == TaskItemStatus.COMPLETE:   return 'x' 
        if self.status == TaskItemStatus.UNKNOWN:    return '?'

    def children(self):
        return [ self.text ]

    def is_checked(self):
        return self.status == TaskItemStatus.COMPLETE or self.status == TaskItemStatus.UNKNOWN

    def __str__(self) -> str:
        return f"[{self.symbol()}] {str(self.text)}"

class TaskList(MarkdownElement):
    """ A list of tasks to complete """
    def __init__(self, items: List[TaskItem]):
        self.items = items

    def children(self):
        return self.items

    def __str__(self) -> str:
        return '\n'.join(map(str, self.items))

