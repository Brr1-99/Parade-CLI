from dataclasses import dataclass
from card import Card

@dataclass
class Player:
    name: str
    hand: list[Card]
    cards: list[Card] 


    def __init__(self, name, hand, cards) -> None:
        self.name = name
        self.hand = hand
        self.cards = cards
    