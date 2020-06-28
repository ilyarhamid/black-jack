from card_deck.card import Card
import numpy as np


def build_deck(num: int = 1, joker: bool = False):
    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suites = ["Club", "Spade", "Diamond", "Heart"]
    card_list = [Card(v, s) for v in values for s in suites]
    if joker:
        card_list.append(Card("Joker", "Big"))
        card_list.append(Card("Joker", "Small"))
    return np.array(card_list * num)


class Deck(object):
    def __init__(self, num_pair: int = 1, joker: bool = False) -> None:
        self.joker = joker
        self.num_pair = num_pair
        self.deck = build_deck(num_pair, joker=joker)
        self.original = len(self.deck)
        self.count = 0

    def shuffle(self) -> None:
        np.random.shuffle(self.deck)

    def deal(self) -> Card:
        c = self.deck[0]
        self.deck = np.delete(self.deck, 0)
        if c.value in ["2", "3", "4", "5", "6"]:
            self.count += 1
        if c.value in ["10", "J", "Q", "K", "A"]:
            self.count -= 1
        return c

    def refresh(self):
        self.deck = build_deck(self.num_pair, joker=self.joker)
