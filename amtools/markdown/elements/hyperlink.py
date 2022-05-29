
class Hyperlink:
    def __init__(self, text: str, addr :str):
        self.text = text
        self.addr = addr

    def __str__(self) -> str:
        return "[" + self.text + "](@" + self.addr + ")"

