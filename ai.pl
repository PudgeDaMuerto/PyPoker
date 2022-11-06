% Artificial Intelligence for Poker Game on SWI-Prolog

:- use_module(library(random)).

blind(25).
aggressive_m(2).
soft_m(1.4).
random_m(X):- random(1, 3, R), R == 1 -> aggressive_m(X) ; soft_m(X).

high_rank(14).
high_rank(13).
high_rank(12).
high_rank(11).

low_rank(2).
low_rank(3).
low_rank(4).
low_rank(5).

royal_flush(1).
straight_flush(2).
four_of_a_kind(3).
full_house(4).
flush(5).
straight(6).
three_of_a_kind(7).
two_pair(8).
pair(9).
high_card(10).

has_comb_1(X):- royal_flush(X);straight_flush(X);four_of_a_kind(X);full_house(X);flush(X);
    straight(X);three_of_a_kind(X);two_pair(X);pair(X).

has_comb(X):- has_comb_1(X), !.

not_low(Card):- \+ low_rank(Card).

double(X, Y):- X == Y.

% M - multiplier
bet(M, X):- blind(B), Blind is B,  X is integer((Blind * M)).

preflop_raise_1(Card1, Card2, X):- (high_rank(Card1), high_rank(Card2) ; double(Card1, Card2)),
    								random_m(M), bet(M, X), !.

preflop_raise_2(Card1, Card2, X):- high_rank(Card1), high_rank(Card2), double(Card1, Card2),
    								aggressive_m(B), bet(B, X), !.

preflop_raise(Card1, Card2, X):- random(1, 3, R), R == 1 -> preflop_raise_1(Card1, Card2, X) ;
    								preflop_raise_2(Card1, Card2, X).

% Call when some player raise in preflop
% Val is value is how many times bid was increased
preflop_call(Card1, Card2, Val):- Val < 4 -> (not_low(Card1) ; not_low(Card2)) ; (not_low(Card1), not_low(Card2)).

flop_raise_1(Rank, X):- high_card(R), Rank<R, random_m(M), bet(M, X).
flop_raise_2(Rank, X):- pair(R), Rank<R, random_m(M), bet(M, X).
flop_raise_3(Rank, X):- two_pair(R), Rank<R, random_m(M), bet(M, X).
flop_raise(Rank, X):- random(1, 4, R), (R == 1 -> flop_raise_1(Rank, X) ; R == 2 -> flop_raise_2(Rank, X) ; flop_raise_3(Rank, X)).

flop_fold(Card1, Card2, Rank):- pair(R), Rank>R, low_rank(Card1), low_rank(Card2), !.
flop_call(Card1, Card2, Rank):- \+ flop_fold(Card1, Card2, Rank).
flop_call_more(Card1, Card2, Rank, Val):- Val < 4 -> ((not_low(Card1) ; not_low(Card2)), ! ; high_card(R), Rank<R, !) ; high_card(R), Rank<R, !.

turn_raise(Rank, X):- flop_raise(Rank, X), !.
turn_call(Card1, Card2, Rank):- pair(R), Rank<R, (high_rank(Card1) ; high_rank(Card2)), !.
turn_fold(Card1, Card2, Rank):- \+ turn_call(Card1, Card2, Rank), !.
turn_call_more(Card1, Card2, Rank, Val):- Val < 4 -> ((high_rank(Card1) ; high_rank(Card2)), ! ; high_card(R), Rank<R, !) ; high_rank(R), Rank<R, !.

river_raise(Rank, X):- flop_raise(Rank, X), !.
river_call(Card1, Card2, Rank):- turn_call(Card1, Card2, Rank), !.
river_fold(Card1, Card2, Rank):- turn_fold(Card1, Card2, Rank), !.
river_call_more(Card1, Card2, Rank, Val):- Val < 4 -> ((high_rank(Card1), high_rank(Card2)), ! ; high_card(R), Rank<R, !) ; pair(R), Rank<R, !.
