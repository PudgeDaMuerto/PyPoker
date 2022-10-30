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
        self.rank = None
        self.comb = None
        self.money = START_MONEY

    @staticmethod
    def _combination(all_cards: list[Card]):

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
            return Rank.STRAIGHT_FLUSH, r[0]
        if r := _is_four_of_a_kind():
            return Rank.FOUR_OF_A_KIND, r
        if r := _is_full_house():
            return Rank.FULL_HOUSE, (r[0], r[1])
        if r := flush:
            return Rank.FLUSH, r
        if r := straight:
            return Rank.STRAIGHT, r[0]
        if r := _is_three_of_a_kind():
            return Rank.THREE_OF_A_KIND, r
        if r := _is_two_pair():
            return Rank.TWO_PAIR, (r[0], r[1])
        if r := _is_pair():
            return Rank.PAIR, r
        return Rank.HIGH_CARD, max(all_cards)

    def hand_rank(self, __table):
        cards_pool = self.hand + __table.hand
        self.rank, self.comb = self._combination(cards_pool)

    def __repr__(self):
        return self.name


class Queue:
    def __init__(self, items: list):
        self.list = items

    def r_push(self, item):
        self.list.append(item)

    def l_push(self, item):
        self.list.insert(0, item)

    def r_pop(self):
        return self.list.pop()

    def l_pop(self):
        return self.list.pop(0)

    def r_move(self):
        self.list = [self.list.pop()] + self.list

    def l_move(self):
        self.list += [self.list.pop(0)]

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return self.list


class PlayersQueue(Queue):
    def __init__(self, items: list):
        super().__init__(items)

    def get_dealer(self) -> Player:
        return self.list[-3]

    def get_s_blind(self) -> Player:
        return self.list[-2]

    def get_b_blind(self) -> Player:
        return self.list[-1]


def _best_hands(*players: Player) -> list[Player]:
    """
    Return players with min rank
    """
    min_rank = 11
    players_with_min_rank = []
    for p in players:
        if p.rank.value < min_rank:
            min_rank = p.rank.value

    for p in players:
        if p.rank.value == min_rank:
            players_with_min_rank.append(p)

    return players_with_min_rank


def is_lower_straight(player: Player) -> bool:
    if (player.rank == Rank.STRAIGHT or player.rank == Rank.STRAIGHT_FLUSH) \
            and player.comb[0] == 14 \
            and player.comb[1] == 5:
        return True
    else:
        return False


def _best_straight(*players: Player) -> list[Player]:
    high_rank = 1
    p_with_better_straight = []
    for p in players:
        card = 1 if is_lower_straight(p) else 0
        if p.comb[card] > high_rank:
            high_rank = p.comb[card]

    for p in players:
        card = 1 if is_lower_straight(p) else 0
        if p.comb[card] == high_rank:
            p_with_better_straight.append(p)

    return p_with_better_straight


def _best_full_house(*players: Player) -> list[Player]:
    max_three = 1
    p_with_best_full_house = []
    for p in players:
        if p.comb[0] > max_three:
            max_three = p.comb[0]
    for p in players:
        if p.comb[0] == max_three:
            p_with_best_full_house.append(p)

    return p_with_best_full_house


def _best_flush(*players: Player) -> list[Player]:
    players_max_cards = [p.comb[0] for p in players]
    max_card = max(players_max_cards)
    p_with_best_flush = []
    for p in players:
        if p.comb[0].val == max_card:
            p_with_best_flush.append(p)
    return p_with_best_flush


def _kicker(player: Player):
    free_cards = []
    for card in player.hand:
        if card not in player.comb:
            free_cards.append(card)
    return max(free_cards)


def _pocket_card(player: Player):
    p_kicker = _kicker(player)
    for card in player.hand:
        if card not in player.comb and card != p_kicker:
            return card


def _is_shared_kicker(table: Table, *players: Player):
    free_table_cards = []
    for card in table.hand:
        if card not in players[0].comb:
            free_table_cards.append(card)

    kickers = [_kicker(p) for p in players]
    table_mb_kickers = []
    for table_card in free_table_cards:
        i = 0
        for kicker in kickers:
            if table_card > kicker:
                i += 1
        if i == len(kickers):
            table_mb_kickers.append(table_card)

    if table_mb_kickers:
        return max(table_mb_kickers)

    return False


def _winner_when_combs_same(*players):
    kickers = [_kicker(p) for p in players]
    max_kicker = max(kickers)

    p_with_max_kicker = []
    for p in players:
        if _kicker(p) == max_kicker:
            p_with_max_kicker.append(p)

    if len(p_with_max_kicker) == 1:
        return p_with_max_kicker[0]

    if None in [_pocket_card(p) for p in p_with_max_kicker]:
        return p_with_max_kicker

    max_pocket = 1
    for p in p_with_max_kicker:
        if (card := _pocket_card(p)) and card > max_pocket:
            max_pocket = card

    p_with_max_pocket = []
    for p in p_with_max_kicker:
        if (card := _pocket_card(p)) and card == max_pocket:
            p_with_max_pocket.append(p)

    return p_with_max_pocket


def _best_four_of_a_kind(table, *players):
    max_rank = 1
    for p in players:
        if p.comb[1][0] > max_rank:
            max_rank = p.comb[1][0]

    p_with_best = []
    for p in players:
        if p.comb[1][0] == max_rank:
            p_with_best.append(p)

    if len(p_with_best) == 1:
        return p_with_best[0]

    if _is_shared_kicker(table, *players):
        return p_with_best

    return _winner_when_combs_same(p_with_best)


def rank_comparison(table: Table, *players: Player):
    p_with_best_hands = _best_hands(*players)
    ps_rank = p_with_best_hands[0].rank
    if len(p_with_best_hands) == 1:
        return p_with_best_hands[0]
    else:
        match ps_rank:
            case Rank.ROYAL_FLUSH:
                return p_with_best_hands
            case Rank.STRAIGHT_FLUSH:
                return _best_straight(*p_with_best_hands)
            case Rank.STRAIGHT:
                return _best_straight(*p_with_best_hands)
            case Rank.FULL_HOUSE:
                return _best_full_house(*p_with_best_hands)
            case Rank.FLUSH:
                return _best_flush(*p_with_best_hands)
            case Rank.FOUR_OF_A_KIND:
                return _best_four_of_a_kind(table, *p_with_best_hands)
        # TODO: cases for other combinations


if __name__ == '__main__':
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

        if player.rank == Rank.FOUR_OF_A_KIND:
            flag = False

        k += 1

    # table.hand = [Card(3, Suits.S), Card(2, Suits.S), Card(6, Suits.C), Card(5, Suits.D), Card(14, Suits.C)]
    # player.hand = [Card(4, Suits.S), Card(5, Suits.H)]
    # player.hand_rank(table)
    print(k)
    print(table.hand)
    print(player.hand)
    print(player.rank)
    print(player.comb)
    print('kicker:', _kicker(player))
