from pyswip import Prolog
from enum import Enum


class State(Enum):
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


prolog = Prolog()
prolog.consult("ai.pl")


def set_blind(blind: int):
    prolog.assertz(f"blind({blind})")


def preflop_raise(player_cards) -> int | bool:
    q = list(prolog.query(f"preflop_raise({player_cards[0].val}, {player_cards[1].val}, X)"))
    if q:
        return q[0]['X']
    else:
        return False


def preflop_call(player_cards, bet):
    blind = list(prolog.query("blind(X)"))[0]['X']
    val = bet/blind

    q = list(prolog.query(f"preflop_call({player_cards[0].val}, {player_cards[1].val}, {val})"))

    return bool(q)


def state_raise(rank, state: State):
    q = list(prolog.query(f"{state.value}_raise({rank.value}, X)"))
    if q:
        return q[0]['X']
    else:
        return False


def state_fold(player_cards, rank, state: State):
    q = list(prolog.query(f"{state.value}_fold({player_cards[0].val}, {player_cards[1].val}, {rank.value})"))

    return bool(q)


def state_call(player_cards, rank, state: State):
    q = list(prolog.query(f"{state.value}_call({player_cards[0].val}, {player_cards[1].val}, {rank.value})"))

    return bool(q)


def state_call_more(player_cards, rank, bet, state: State):
    blind = list(prolog.query("blind(X)"))[0]['X']
    val = bet / blind

    q = list(prolog.query(f"{state.value}_call_more({player_cards[0].val}, {player_cards[1].val}, {rank.value}, {val})"))

    return bool(q)
