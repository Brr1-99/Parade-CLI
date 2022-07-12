import random
from card import Card
from dataclasses import dataclass

@dataclass
class Deck:
    cards: list[Card]

    def __init__(self, cards) -> None:
        self.cards = cards
    
    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self, n: int= 1) -> list:
        draws = []
        for _ in range(n):
            draws.append(self.cards.pop())
        return draws
