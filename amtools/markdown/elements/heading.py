
class Heading:
    """ A heading in a markdown document """

    def __init__(self, weight: int, title: str):
        self.weight = weight
        self.title  = title

    def __str__(self) -> str:
        return f"[H{self.weight}] {self.title}"
