from card_deck.card import Card
from typing import List, Tuple
import numpy as np

value_dict = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11
}


class Hand(object):
    def __init__(self, cards: List[Card]) -> None:
        self.cards = cards
        self.bet = 0
        self.action = "Stand"

    def best_value(self) -> Tuple[int, str]:
        # take values of all cards, Ace is assumed 11 initially
        v_list = np.array([value_dict[c.value] for c in self.cards])
        best_value = sum(v_list)  # sum all the values
        if 11 in v_list:
            if best_value <= 21:  # If there is Ace in hand and value is smaller than 21, return soft sum value
                return best_value, "Soft"
            else:  # If sum value exceeds 21 with Aces in hand, minus 10 for each Ace until the best score < 21
                for v in v_list:
                    if v == 11:
                        best_value -= 10
                        if best_value <= 21:
                            return best_value, "Soft"
        else:  # If there is no Ace, return the hard sum value
            return best_value, "Hard"


class Player(object):
    def __init__(self):
        self.money = 0
        self.hands = []
