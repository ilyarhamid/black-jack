from card_deck.deck import Deck
from player.player import Player
from table.game import Game


class Table(object):
    def __init__(self,
                 n_game: int,  # Number of simulated game
                 n_pair: int = 8,  # How many pairs of cards in the deck
                 n_player: int = 3,  # Number of mock players
                 rule: str = "H17",  # H17: Dealer must hit on soft 17; S17: Dealer stands on soft 17.
                 betting: str = "flat",  # flat: flat betting; MIT: MIT BlackJack team betting strategy
                 black_jack_pay: float = 3/2,  # Usually 3/2 or 6/5
                 shoe_pct: float = 0.3):  # When to shuffle the shoe
        self.n_game = n_game
        self.rule = rule
        self.betting = betting
        self.black_jack_pay = black_jack_pay
        self.deck = Deck(n_pair)
        self.dealer = Player()
        self.key_player = Player()
        self.players = [Player() for i in range(n_player)]
        self.shoe_pct = shoe_pct
