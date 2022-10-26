from dataclasses import dataclass
import random
from enum import Enum

START_MONEY = 1000


class Rank(Enum):
    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_OF_A_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_OF_A_KIND = 7
    TWO_PAIR = 8
    PAIR = 9
    HIGH_CARD = 10


class Suits(Enum):
    H = "hearts"
    C = "clubs"
    S = "spades"
    D = "diamonds"


@dataclass
class Card:
    val: int
    suit: Suits

    def __repr__(self):
        return f'{self.val} of {self.suit.value}'

    def __eq__(self, other):
        if type(other) == Card:
            if self.val == other.val and self.suit == other.suit:
                return True
            else:
                return False
        else:
            return self.val == other

    def __ne__(self, other):
        if type(other) == Card:
            if self.val != other.val or self.suit != other.suit:
                return True
            else:
                return False
        else:
            return self.val != other

    def __lt__(self, other):
        if type(other) == Card:
            return self.val < other.val
        else:
            return self.val == other

    def __gt__(self, other):
        if type(other) == Card:
            return self.val > other.val
        else:
            return self.val > other

    def __le__(self, other):
        if type(other) == Card:
            return self.val <= other.val
        else:
            return self.val <= other

    def __ge__(self, other):
        if type(other) == Card:
            return self.val >= other.val
        else:
            return self.val >= other

    def __hash__(self):
        return self.val


class Deck:
    def __init__(self):
        self.cards = []
        self.__build()

    def __build(self):
        for suit in Suits:
            for val in range(2, 15):
                self.cards.append(Card(val, suit))

    def shuffle(self):
        for card in range(len(self.cards) - 1, 0, -1):
            random_card = random.randint(0, card)
            self.cards[card], self.cards[random_card] = self.cards[random_card], self.cards[card]

    def draw(self):
        return self.cards.pop()

    def refresh(self):
        self.__init__()


class Table:
    def __init__(self):
        self.hand = []

    def draw(self, __deck, num_of_cards):
        for _ in range(num_of_cards):
            self.hand.append(__deck.draw())

    def clear(self):
        self.hand = []


class Player(Table):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.rank = (None, None)
        self.money = START_MONEY

    @staticmethod
    def combination(all_cards: list[Card]):

        def _set_cards_val(cards: list[Card]):
            res = []
            for card in cards:
                if card.val not in res:
                    res.append(card)

            return res

        def _is_flush():
            for suit in Suits:
                count = 0
                comb = []
                for card in sorted(all_cards, reverse=True):
                    if card.suit == suit:
                        count += 1
                        comb.append(card)
                if count >= 5:
                    return comb
            return False

        def _is_straight():
            folded = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
            straights = [set(folded[n:n + 5]) for n in range(len(folded) - 4)]

            lowest_straight = {14, 2, 3, 4, 5}

            def is_straight_sub(five_cards):
                if set(five_cards) in straights:
                    return five_cards
                return False

            found_straights = []
            cards_set = sorted(_set_cards_val(all_cards), reverse=True)
            for i, j in zip([0, 1, 2], [5, 6, 7]):
                sorted_cards_val = cards_set[i:j]
                if r := is_straight_sub(sorted_cards_val):
                    found_straights.append(r)

            if lowest_straight <= set(all_cards):
                five_place = cards_set.index(5)
                found_straights.append([cards_set[0], *cards_set[five_place:]])

            if found_straights:
                return found_straights

            return False

        straight = _is_straight()
        flush = _is_flush()

        def _is_royal_flush():
            if r := _is_straight_flush():
                for i in r:
                    if i[0] == 14 and i[1] == 13:
                        return i
            return False

        def _is_straight_flush():
            found_straight_flushes = []
            if straight and flush:
                for i in straight:
                    if set(i) <= set(flush):
                        found_straight_flushes.append(i)

            if found_straight_flushes:
                return found_straight_flushes
            return False

        cards_val = [card.val for card in all_cards]

        def _cards_count():
            cards_set = set(cards_val)
            cards_d = {card: 0 for card in cards_set}
            for card in cards_d:
                cards_d[card] += cards_val.count(card)

            return cards_d

        cards_dict = _cards_count()

        def _doubles(rank: int):
            res = []
            for k, v in cards_dict.items():
                if v == rank:
                    res.append(k)
            if res:
                return res

            return False

        def _is_four_of_a_kind():
            return _doubles(4)

        def _is_full_house():
            if _is_three_of_a_kind() and _is_pair():
                set_ = _is_three_of_a_kind()
                pair = max(_is_pair())
                if set_ and pair:
                    return *set_, pair
            return False

        def _is_three_of_a_kind():
            return _doubles(3)

        def _is_two_pair():
            pairs = _doubles(2)
            if pairs and len(pairs) >= 2:
                pairs.sort()
                return pairs[-1], pairs[-2]
            return False

        def _is_pair():
            return _doubles(2)

        if r := _is_royal_flush():
            return Rank.ROYAL_FLUSH, r
        if r := _is_straight_flush():
            return Rank.STRAIGHT_FLUSH, r
        if r := _is_four_of_a_kind():
            return Rank.FOUR_OF_A_KIND, r
        if r := _is_full_house():
            return Rank.FULL_HOUSE, r[0], r[1]
        if r := flush:
            return Rank.FLUSH, r
        if r := straight:
            return Rank.STRAIGHT, r
        if r := _is_three_of_a_kind():
            return Rank.THREE_OF_A_KIND, r
        if r := _is_two_pair():
            return Rank.TWO_PAIR, r[0], r[1]
        if r := _is_pair():
            return Rank.PAIR, r
        return Rank.HIGH_CARD, max(all_cards)

    def hand_rank(self, __table):
        cards_pool = self.hand + __table.hand
        self.rank = self.combination(cards_pool)


# TODO: class Queue for players


player = Player("Maxim")
table = Table()

k = 0
flag = True
while flag is True:
    deck = Deck()
    deck.shuffle()

    table.clear()
    player.clear()

    table.draw(deck, 5)
    player.draw(deck, 2)

    player.hand_rank(table)

    if player.rank[0] == Rank.PAIR:
        flag = False

    k += 1


# table.hand = [Card(3, Suits.S), Card(2, Suits.S), Card(5, Suits.C), Card(5, Suits.D), Card(14, Suits.C)]
# player.hand = [Card(4, Suits.S), Card(5, Suits.H)]
# player.hand_rank(table)
print(k)
print(table.hand)
print(player.hand)
print(player.rank)
