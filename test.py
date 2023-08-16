import unittest
from cards import Player, Table, Card, Suits, \
    _best_straight, _best_flush, _kicker, _is_shared_kicker, \
    _pocket_card, _winner_when_combs_same, _best_two_pair, _best_pair, \
    _best_high_card


class DefaultSetUp(unittest.TestCase):
    def setUp(self):
        self.test_player_1 = Player("Test1")
        self.test_player_2 = Player("Test2")
        self.table = Table()


class TestBestStraight(DefaultSetUp):
    def test_best_straight_1(self):
        """
        Case when test_player_2 have straight to 7 and test_player_1 have straight to 6
        """
        self.table.hand = [
            Card(2, Suits.S),
            Card(3, Suits.S),
            Card(4, Suits.C),
            Card(5, Suits.D),
            Card(12, Suits.C)
        ]
        self.test_player_1.hand = [Card(6, Suits.S), Card(11, Suits.H)]
        self.test_player_2.hand = [Card(6, Suits.S), Card(7, Suits.H)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_straight(self.test_player_1, self.test_player_2),
            [self.test_player_2]
        )

    def test_best_straight_2(self):
        """
        Case when players have same straights
        """
        self.table.hand = [
            Card(2, Suits.S),
            Card(3, Suits.S),
            Card(4, Suits.C),
            Card(5, Suits.D),
            Card(12, Suits.C)
        ]
        self.test_player_1.hand = [Card(6, Suits.D), Card(11, Suits.H)]
        self.test_player_2.hand = [Card(6, Suits.S), Card(11, Suits.D)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_straight(self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )

    def test_best_straight_3(self):
        """
        Case when test_player_1 have lower straight to 5 and test_player_2 have straight to 6
        """
        self.table.hand = [
            Card(2, Suits.S),
            Card(3, Suits.S),
            Card(4, Suits.C),
            Card(7, Suits.D),
            Card(14, Suits.C)
        ]
        self.test_player_1.hand = [Card(5, Suits.S), Card(11, Suits.H)]
        self.test_player_2.hand = [Card(5, Suits.S), Card(6, Suits.H)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_straight(self.test_player_1, self.test_player_2),
            [self.test_player_2]
        )

    def test_best_straight_4(self):
        """
        Case when players have lower straights
        """
        self.table.hand = [
            Card(2, Suits.S),
            Card(3, Suits.S),
            Card(4, Suits.C),
            Card(7, Suits.D),
            Card(14, Suits.C)

        ]
        self.test_player_1.hand = [Card(5, Suits.S), Card(11, Suits.H)]
        self.test_player_2.hand = [Card(5, Suits.S), Card(11, Suits.H)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_straight(self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )


class TestBestFlush(DefaultSetUp):
    def setUp(self):
        self.test_player_1 = Player("Test1")
        self.test_player_2 = Player("Test2")
        self.table = Table()

    def test_best_flush_1(self):
        """
        Case when players have same flushes (impossible situation)
        """
        self.table.hand = [
            Card(2, Suits.S),
            Card(3, Suits.S),
            Card(4, Suits.C),
            Card(7, Suits.S),
            Card(14, Suits.C)
        ]
        self.test_player_1.hand = [Card(5, Suits.S), Card(11, Suits.S)]
        self.test_player_2.hand = [Card(5, Suits.S), Card(11, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_flush(self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )

    def test_best_flush_2(self):
        """
        Case when test_player_2 have a more valuable card in combination, but test_player_1 have most valuable
        card in hand
        """
        self.table.hand = [
            Card(2, Suits.S),
            Card(3, Suits.S),
            Card(4, Suits.S),
            Card(7, Suits.S),
            Card(14, Suits.C)
        ]
        self.test_player_1.hand = [Card(5, Suits.S), Card(12, Suits.D)]
        self.test_player_2.hand = [Card(5, Suits.S), Card(11, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_flush(self.test_player_1, self.test_player_2),
            [self.test_player_2]
        )


class TestKicker(DefaultSetUp):
    def setUp(self):
        self.test_player_1 = Player("Test1")
        self.test_player_2 = Player("Test2")
        self.table = Table()

    def test_kicker_1(self):
        """
        Case when player has two cards, that don`t belong to combination
        """
        self.table.hand = [
            Card(5, Suits.D),
            Card(5, Suits.C),
            Card(12, Suits.H),
            Card(7, Suits.S),
            Card(12, Suits.C)
        ]
        self.test_player_1.hand = [Card(14, Suits.C), Card(11, Suits.S)]
        self.test_player_1.hand_rank(self.table)

        self.assertEqual(_kicker(self.test_player_1), Card(14, Suits.C))

    def test_kicker_2(self):
        """
        Case when player has one card, that don`t belong to combination
        """
        self.table.hand = [
            Card(5, Suits.D),
            Card(10, Suits.C),
            Card(12, Suits.H),
            Card(7, Suits.S),
            Card(12, Suits.C)
        ]
        self.test_player_1.hand = [Card(13, Suits.C), Card(10, Suits.S)]
        self.test_player_1.hand_rank(self.table)

        self.assertEqual(_kicker(self.test_player_1), Card(13, Suits.C))


class TestSharedKicker(DefaultSetUp):
    def test_is_shared_kicker_1(self):
        """
        Case when table have two free cards
        """
        self.table.hand = [
            Card(5, Suits.D),
            Card(7, Suits.C),
            Card(12, Suits.H),
            Card(13, Suits.S),
            Card(12, Suits.C)
        ]
        self.test_player_1.hand = [Card(7, Suits.S), Card(3, Suits.D)]
        self.test_player_2.hand = [Card(7, Suits.S), Card(3, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _is_shared_kicker(self.table, self.test_player_1, self.test_player_2),
            Card(13, Suits.S)
        )


class TestPocketCard(DefaultSetUp):
    def test_pocket_card_1(self):
        """
        Case when players have same kickers
        """
        self.table.hand = [
            Card(7, Suits.H),
            Card(5, Suits.S),
            Card(2, Suits.H),
            Card(9, Suits.H),
            Card(7, Suits.C)
        ]
        self.test_player_1.hand = [Card(13, Suits.S), Card(12, Suits.D)]
        self.test_player_2.hand = [Card(11, Suits.C), Card(13, Suits.H)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _pocket_card(self.test_player_1),
            Card(12, Suits.D)
        )
        self.assertEqual(
            _pocket_card(self.test_player_2),
            Card(11, Suits.C)
        )


class TestWinnerWhenCombsSame(DefaultSetUp):
    def test_winner_when_combs_same_1(self):
        """
        Case when players have same kickers but diff pocket cards
        """
        self.table.hand = [
            Card(7, Suits.H),
            Card(5, Suits.S),
            Card(2, Suits.H),
            Card(9, Suits.H),
            Card(7, Suits.C)
        ]
        self.test_player_1.hand = [Card(13, Suits.S), Card(12, Suits.D)]
        self.test_player_2.hand = [Card(11, Suits.C), Card(13, Suits.H)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _winner_when_combs_same(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1]
        )

    def test_winner_when_combs_same_2(self):
        """
        Case when players have same kickers
        """
        self.table.hand = [
            Card(7, Suits.H),
            Card(5, Suits.S),
            Card(2, Suits.H),
            Card(9, Suits.H),
            Card(7, Suits.C)
        ]
        self.test_player_1.hand = [Card(7, Suits.S), Card(12, Suits.D)]
        self.test_player_2.hand = [Card(7, Suits.C), Card(13, Suits.H)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _winner_when_combs_same(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_2]
        )

    def test_winner_when_combs_same_3(self):
        """
        Case when players have shared kicker
        """
        self.table.hand = [
            Card(3, Suits.H),
            Card(5, Suits.S),
            Card(6, Suits.H),
            Card(9, Suits.H),
            Card(8, Suits.C)
        ]
        self.test_player_1.hand = [Card(3, Suits.S), Card(4, Suits.D)]
        self.test_player_2.hand = [Card(3, Suits.C), Card(4, Suits.H)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _winner_when_combs_same(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )

    def test_winner_when_combs_same_4(self):
        """
        Case when players don`t have kickers
        """
        self.table.hand = [
            Card(2, Suits.D),
            Card(3, Suits.C),
            Card(7, Suits.S),
            Card(12, Suits.D),
            Card(13, Suits.S)
        ]
        self.test_player_1.hand = [Card(2, Suits.S), Card(3, Suits.H)]
        self.test_player_2.hand = [Card(2, Suits.H), Card(3, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _winner_when_combs_same(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )


class TestBestTwoPair(DefaultSetUp):
    def test_best_two_pair_1(self):
        """
        Case when players have two pairs, but test_player_1 have one better
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(11, Suits.C),
            Card(9, Suits.C),
            Card(11, Suits.S)
        ]
        self.test_player_1.hand = [Card(9, Suits.D), Card(10, Suits.H)]
        self.test_player_2.hand = [Card(2, Suits.H), Card(3, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_two_pair(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1]
        )

    def test_best_two_pair_2(self):
        """
        Case when players have two pairs, but test_player_2 have one better card, which isn`t highest
        """
        self.table.hand = [
            Card(4, Suits.S),
            Card(10, Suits.C),
            Card(5, Suits.S),
            Card(9, Suits.H),
            Card(13, Suits.D)
        ]
        self.test_player_1.hand = [Card(4, Suits.D), Card(13, Suits.H)]
        self.test_player_2.hand = [Card(9, Suits.D), Card(13, Suits.C)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_two_pair(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_2]
        )


class TestBestPair(DefaultSetUp):
    def test_best_pair_1(self):
        """
        Case when test_player_1 have better pair
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(11, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(3, Suits.D), Card(10, Suits.H)]
        self.test_player_2.hand = [Card(3, Suits.H), Card(9, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_pair(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1]
        )

    def test_best_pair_2(self):
        """
        Case when players have same pairs and kickers
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(11, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(3, Suits.D), Card(10, Suits.H)]
        self.test_player_2.hand = [Card(3, Suits.H), Card(10, Suits.C)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_pair(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )

    def test_best_pair_3(self):
        """
        Case when players have same kickers but test_player_1 have better pocket card
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(10, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(12, Suits.D), Card(8, Suits.H)]
        self.test_player_2.hand = [Card(12, Suits.H), Card(3, Suits.C)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_pair(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1]
        )

    def test_best_pair_4(self):
        """
        Case when players have same kickers but test_player_1 have better pocket card
        """
        self.table.hand = [Card(2, Suits.H), Card(4, Suits.H), Card(12, Suits.C), Card(9, Suits.C), Card(10, Suits.S)]
        self.test_player_1.hand = [Card(12, Suits.D), Card(8, Suits.H)]
        self.test_player_2.hand = [Card(12, Suits.H), Card(3, Suits.C)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_pair(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1]
        )


class TestBestHighCard(DefaultSetUp):
    def test_best_high_card_1(self):
        """
        Case when players have same kickers
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(11, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(12, Suits.D), Card(3, Suits.H)]
        self.test_player_2.hand = [Card(12, Suits.H), Card(3, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_high_card(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )

    def test_best_high_card_2(self):
        """
        Case when test_player_2 have better kicker
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(11, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(12, Suits.D), Card(3, Suits.H)]
        self.test_player_2.hand = [Card(12, Suits.H), Card(5, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _best_high_card(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_2]
        )

    def test_best_high_card_3(self):
        """
        Case when players have shared kicker
        """
        self.table.hand = [
            Card(5, Suits.H),
            Card(4, Suits.H),
            Card(11, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(12, Suits.D), Card(3, Suits.H)]
        self.test_player_2.hand = [Card(12, Suits.H), Card(2, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertTrue(
            _is_shared_kicker(self.table, self.test_player_1, self.test_player_2)
        )
        self.assertEqual(
            _best_high_card(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )

    def test_best_high_card_4(self):
        """
        Case when players have same kickers, but test_player_1 have better pocket card
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(12, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(11, Suits.D), Card(5, Suits.H)]
        self.test_player_2.hand = [Card(11, Suits.H), Card(3, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertGreater(
            _pocket_card(self.test_player_1),
            _pocket_card(self.test_player_2)
        )
        self.assertEqual(
            _kicker(self.test_player_1).val,
            _kicker(self.test_player_2).val
        )
        self.assertEqual(
            _best_high_card(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1]
        )

    def test_best_high_card_5(self):
        """
        Case when players have same kickers and same pocket cards
        """
        self.table.hand = [
            Card(2, Suits.H),
            Card(4, Suits.H),
            Card(12, Suits.C),
            Card(9, Suits.C),
            Card(10, Suits.S)
        ]
        self.test_player_1.hand = [Card(11, Suits.D), Card(3, Suits.H)]
        self.test_player_2.hand = [Card(11, Suits.H), Card(3, Suits.S)]
        self.test_player_1.hand_rank(self.table)
        self.test_player_2.hand_rank(self.table)

        self.assertEqual(
            _pocket_card(self.test_player_1).val,
            _pocket_card(self.test_player_2).val
        )
        self.assertEqual(
            _best_high_card(self.table, self.test_player_1, self.test_player_2),
            [self.test_player_1, self.test_player_2]
        )
