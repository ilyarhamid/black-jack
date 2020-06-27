from card_deck.card import Card
from typing import List, Tuple
import pandas as pd

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
strategy_path = "/Users/ilyarhamid/ilyar/work/projects/black-jack/basic_strategies/"
df_hard = pd.read_excel(strategy_path + "basic_strategy_hard.xlsx").set_index(0)
df_soft = pd.read_excel(strategy_path + "basic_strategy_soft.xlsx").set_index(0)
df_pair = pd.read_excel(strategy_path + "basic_strategy_pair.xlsx").set_index(0)


class Hand(object):
    def __init__(self, cards: List[Card]) -> None:
        self.cards = cards
        self.bet = 0
        self.action = "Stand"
        self.strategy = {"Hard": df_hard, "Soft": df_soft, "Pair": df_pair}

    def best_value(self) -> Tuple[int, str]:
        v_list = [value_dict[c.value] for c in self.cards]
        best_value = 0
        ace_count = 0
        for v in v_list:
            if v == 1:
                ace_count += 1
                best_value -= 10
            best_value += v
        if ace_count == 0:
            return best_value, "Hard"
        else:
            if best_value < 12:
                return best_value + 10, "Soft"
            else:
                return best_value, "Hard"

    def get_action(self, dealer_hand: int) -> str:
        if len(self.cards) == 2:
            if self.cards[0].value == self.cards[1].value:
                return self.strategy["Pair"][dealer_hand].loc[value_dict[self.cards[0].value]]
            else:
                val, hard_or_soft = self.best_value()
                return self.strategy[hard_or_soft][dealer_hand][val]
        else:
            val, hard_or_soft = self.best_value()
            if val > 21:
                return "Bust"
            else:
                return self.strategy[hard_or_soft][dealer_hand][val]


class Player(object):
    def __init__(self):
        self.money = 0
        self.hands = [Hand([])]
