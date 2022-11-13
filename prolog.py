from pyswip import Prolog
from enum import Enum


class State(Enum):
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


class Pl:
    def __init__(self):
        self.prolog = Prolog()
        self.prolog.consult("ai.pl")

    # Functions to call functions from prolog
    def state_raise(self, rank, state: State):
        q = list(self.prolog.query(f"{state.value}_raise({rank.value}, X)"))
        if q:
            return q[0]['X']
        else:
            return False

    def state_fold(self, player_cards, rank, state: State):
        q = list(self.prolog.query(f"{state.value}_fold({player_cards[0].val}, {player_cards[1].val}, {rank.value})"))

        return bool(q)

    def state_call(self, player_cards, rank, state: State):
        q = list(self.prolog.query(f"{state.value}_call({player_cards[0].val}, {player_cards[1].val}, {rank.value})"))

        return bool(q)

    def state_call_more(self, player_cards, rank, bet, state: State):
        blind = list(self.prolog.query("blind(X)"))[0]['X']
        val = bet / blind

        q = list(self.prolog.query(f"{state.value}_call_more({player_cards[0].val}, {player_cards[1].val}, {rank.value}, {val})"))

        return bool(q)

    # Realization of all ai.pl function that I needed to call in game
    def set_blind(self, blind: int):
        self.prolog.assertz(f"blind({blind})")

    def preflop_raise(self, player_cards) -> int | bool:
        q = list(self.prolog.query(f"preflop_raise({player_cards[0].val}, {player_cards[1].val}, X)"))
        if q:
            return q[0]['X']
        else:
            return False

    def preflop_call_more(self, player_cards, bet) -> bool:
        blind = list(self.prolog.query("blind(X)"))[0]['X']
        val = bet/blind

        q = list(self.prolog.query(f"preflop_call_more({player_cards[0].val}, {player_cards[1].val}, {val})"))

        return bool(q)
