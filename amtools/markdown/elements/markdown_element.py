
class MarkdownElement:
    def children(self):
        return []

    def __iter__(self):
        for child in self.children():
            yield child

class EmptyElement(MarkdownElement):
    pass
