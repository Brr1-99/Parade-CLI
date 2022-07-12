from dataclasses import dataclass

@dataclass
class Card:
    value: int
    color: str

    def __init__(self, value, color) -> None:
        self.value = value
        self.color = color