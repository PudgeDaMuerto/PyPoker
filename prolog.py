from pyswip import Prolog
from enum import Enum


class State(Enum):
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


prolog = Prolog()
prolog.consult("ai.pl")


# Functions to call functions from prolog
def __state_raise(rank, state: State):
    q = list(prolog.query(f"{state.value}_raise({rank.value}, X)"))
    if q:
        return q[0]['X']
    else:
        return False


def __state_fold(player_cards, rank, state: State):
    q = list(prolog.query(f"{state.value}_fold({player_cards[0].val}, {player_cards[1].val}, {rank.value})"))

    return bool(q)


def __state_call(player_cards, rank, state: State):
    q = list(prolog.query(f"{state.value}_call({player_cards[0].val}, {player_cards[1].val}, {rank.value})"))

    return bool(q)


def __state_call_more(player_cards, rank, bet, state: State):
    blind = list(prolog.query("blind(X)"))[0]['X']
    val = bet / blind

    q = list(prolog.query(f"{state.value}_call_more({player_cards[0].val}, {player_cards[1].val}, {rank.value}, {val})"))

    return bool(q)


# Realization of all ai.pl function that I needed to call in game
def set_blind(blind: int):
    prolog.assertz(f"blind({blind})")


def preflop_raise(player_cards) -> int | bool:
    q = list(prolog.query(f"preflop_raise({player_cards[0].val}, {player_cards[1].val}, X)"))
    if q:
        return q[0]['X']
    else:
        return False


def preflop_call_more(player_cards, bet):
    blind = list(prolog.query("blind(X)"))[0]['X']
    val = bet/blind

    q = list(prolog.query(f"preflop_call_more({player_cards[0].val}, {player_cards[1].val}, {val})"))

    return bool(q)


# Wrapping functions for communicates with Prolog
def flop_raise(rank):
    __state_raise(rank, State.FLOP)


def turn_raise(rank):
    __state_raise(rank, State.TURN)


def river_raise(rank):
    __state_raise(rank, State.RIVER)


def flop_fold(player_cards, rank):
    __state_fold(player_cards, rank, State.FLOP)


def turn_fold(player_cards, rank):
    __state_fold(player_cards, rank, State.TURN)


def river_fold(player_cards, rank):
    __state_fold(player_cards, rank, State.RIVER)


def flop_call(player_cards, rank):
    __state_call(player_cards, rank, State.FLOP)


def turn_call(player_cards, rank):
    __state_call(player_cards, rank, State.TURN)


def river_call(player_cards, rank):
    __state_call(player_cards, rank, State.RIVER)


def flop_call_more(player_cards, rank, bet):
    __state_call_more(player_cards, rank, bet, State.FLOP)


def turn_call_more(player_cards, rank, bet):
    __state_call_more(player_cards, rank, bet, State.TURN)


def river_call_more(player_cards, rank, bet):
    __state_call_more(player_cards, rank, bet, State.RIVER)
