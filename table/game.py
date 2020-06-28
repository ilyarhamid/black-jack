from typing import List
from player.player import Player, Hand
from card_deck.deck import Deck

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
    "A": 11,
}


class Game(object):
    def __init__(self,
                 dealer: Player,
                 players: List[Player],
                 key_player: Player,
                 initial_deck: Deck,
                 rule: str,
                 betting: str,
                 black_jack_pay: float,
                 shoe_pct: float,
                 log: bool,
                 ) -> None:
        self.dealer = dealer
        self.players = players
        self.key_player = key_player
        self.deck = initial_deck
        self.rule = rule
        self.betting = betting
        self.black_jack_pay = black_jack_pay
        self.shoe_pct = shoe_pct
        self.log = log

    def check_the_shoe(self):
        if len(self.deck.deck) / self.deck.original < self.shoe_pct:
            self.deck.refresh()

    def first_deal(self):
        all_players = [self.dealer, self.key_player]
        all_players.extend(self.players)
        for i in range(2):
            for p in all_players:
                p.hands[0].cards.append(self.deck.deal())

    def player_split(self, p: Player) -> None:
        for h in p.hands:
            act = h.get_action(value_dict[self.dealer.hands[0].cards[0].value])
            if act == "HP" or act == "P":
                p.hands.remove(h)
                p.hands.extend(
                    [
                        Hand([h.cards[0], self.deck.deal()]),
                        Hand([h.cards[1], self.deck.deal()])
                    ]
                )
                self.player_split(p)

    def single_player(self, p: Player, flag=False) -> None:
        self.player_split(p)
        if self.log:
            print("Player Hands Split!")
        h_count = 1
        for h in p.hands:
            if self.log:
                print(f"Hand {h_count}")
            if flag:
                if self.betting == "MIT":
                    true_count = self.deck.count / round(len(self.deck.deck) / 52.0)
                    if true_count > 2:
                        unit = true_count - 1.0
                    else:
                        unit = 1.0
                else:
                    unit = 1.0
                h.bet = unit
                p.money = p.money - unit
            while True:
                act = h.get_action(value_dict[self.dealer.hands[0].cards[0].value])
                if act == "H":
                    h.cards.append(self.deck.deal())
                    if self.log:
                        print(f"Hit: {[c.value for c in h.cards]}")
                if act == "S":
                    if self.log:
                        print(f"Stand: {[c.value for c in h.cards]}")
                    break
                if act == "D":
                    h.cards.append(self.deck.deal())
                    p.money -= h.bet
                    h.bet = h.bet * 2.0
                    if self.log:
                        print(f"Double: {[c.value for c in h.cards]}")
                    break
                if act == "R":  # In case of surrender,
                    p.money += 0.5 * h.bet  # return half of the betting money to the player
                    h.bet = -0.5 * h.bet  # negative value is for marking purpose. This will be turned to positive value
                    if self.log:
                        print(f"Surrender: {[c.value for c in h.cards]}")
                    break
                if act == "Bust":
                    if self.log:
                        print(f"Bust: {[c.value for c in h.cards]}")
                    break

    def player_round(self) -> None:
        if self.log:
            print("----------------- Key Player Turn ---------------")
        self.single_player(self.key_player, flag=True)
        icount = 1
        for ply in self.players:
            if self.log:
                print(f"----------------- Player {icount} Turn ---------------")
            self.single_player(ply)
            icount += 1

    def dealer_round(self) -> None:
        h = self.dealer.hands[0]
        while True:
            val, hard_soft = h.best_value()
            if self.rule == "S17":
                if val < 17:
                    h.cards.append(self.deck.deal())
                    if self.log:
                        print("Dealer Hit!")
                        print([c.value for c in self.dealer.hands[0].cards])
                else:
                    if self.log:
                        print("Dealer Stand")
                        print([c.value for c in self.dealer.hands[0].cards])
                    break
            if self.rule == "H17":
                if val >= 17 and hard_soft == "Hard":
                    if self.log:
                        print("Dealer Stand!")
                        print([c.value for c in self.dealer.hands[0].cards])
                    break
                else:
                    if self.log:
                        print("Dealer Hit!")
                        print([c.value for c in self.dealer.hands[0].cards])
                    h.cards.append(self.deck.deal())

    def wrap_up(self) -> None:
        dealer_value, dealer_mock = self.dealer.hands[0].best_value()
        dealer_black_jack = (dealer_value == 21) and (len(self.dealer.hands[0].cards) == 2)
        for h in self.key_player.hands:
            if h.bet < 0:  # Negative betting value means player surrendered
                h.bet = abs(h.bet)  # change the value to positive
                continue
            hand_value, hand_mock = h.best_value()
            if hand_value == 21 and len(h.cards) == 2:
                if not dealer_black_jack:
                    h.bet = h.bet * (self.black_jack_pay + 1.0)
            elif hand_value > 21:
                h.bet = 0
            else:
                if dealer_value > 21:
                    h.bet = h.bet * 2.0
                else:
                    if dealer_value > hand_value:
                        h.bet = 0.0
                    elif dealer_value < hand_value:
                        h.bet = h.bet * 2.0
            self.key_player.money += h.bet
        #       Clear Hands
        self.dealer.hands = [Hand([])]
        self.key_player.hands = [Hand([])]
        for p in self.players:
            p.hands = [Hand([])]

    def run(self) -> None:
        self.check_the_shoe()
        self.first_deal()
        self.player_round()
        if self.log:
            print("----------------- Dealer Turn ---------------")
        self.dealer_round()
        self.wrap_up()
