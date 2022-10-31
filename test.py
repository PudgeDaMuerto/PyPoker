def _test_best_straight():
    from cards import Player, Table, Card, Suits, _best_straight
    test1 = Player("Test1")
    test2 = Player("Test2")
    table = Table()

    def _test_best_straight_1():
        """
        Case when player Test2 have straight to 7 and player Test1 have straight to 6
        """
        table.hand = [Card(2, Suits.S), Card(3, Suits.S), Card(4, Suits.C), Card(5, Suits.D), Card(12, Suits.C)]
        test1.hand = [Card(6, Suits.S), Card(11, Suits.H)]
        test2.hand = [Card(6, Suits.S), Card(7, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _best_straight(test1, test2) == [test2]

    def _test_best_straight_2():
        """
        Case when players Test2 have same straights
        """
        table.hand = [Card(2, Suits.S), Card(3, Suits.S), Card(4, Suits.C), Card(5, Suits.D), Card(12, Suits.C)]
        test1.hand = [Card(6, Suits.S), Card(11, Suits.H)]
        test2.hand = [Card(6, Suits.S), Card(11, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _best_straight(test1, test2) == [test1, test2]

    def _test_best_straight_3():
        """
        Case when player Test1 have lower straight to 5 and Test2 have straight to 6
        """
        table.hand = [Card(2, Suits.S), Card(3, Suits.S), Card(4, Suits.C), Card(7, Suits.D), Card(14, Suits.C)]
        test1.hand = [Card(5, Suits.S), Card(11, Suits.H)]
        test2.hand = [Card(5, Suits.S), Card(6, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _best_straight(test1, test2) == [test2]

    def _test_best_straight_4():
        """
        Case when players have lower straights
        """
        table.hand = [Card(2, Suits.S), Card(3, Suits.S), Card(4, Suits.C), Card(7, Suits.D), Card(14, Suits.C)]
        test1.hand = [Card(5, Suits.S), Card(11, Suits.H)]
        test2.hand = [Card(5, Suits.S), Card(11, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _best_straight(test1, test2) == [test1, test2]

    _test_best_straight_1()
    _test_best_straight_2()
    _test_best_straight_3()
    _test_best_straight_4()


def _test_best_flush():
    from cards import Player, Table, Card, Suits, _best_flush
    test1 = Player("Test1")
    test2 = Player("Test2")
    table = Table()

    def _test_best_flush_1():
        """
        Case when players have same flushes (impossible situation)
        """
        table.hand = [Card(2, Suits.S), Card(3, Suits.S), Card(4, Suits.C), Card(7, Suits.S), Card(14, Suits.C)]
        test1.hand = [Card(5, Suits.S), Card(11, Suits.S)]
        test2.hand = [Card(5, Suits.S), Card(11, Suits.S)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _best_flush(test1, test2) == [test1, test2]

    def _test_best_flush_2():
        """
        Case when Test2 have a more valuable card in combination, but Test1 have most valuable
        card in hand
        """
        table.hand = [Card(2, Suits.S), Card(3, Suits.S), Card(4, Suits.S), Card(7, Suits.S), Card(14, Suits.C)]
        test1.hand = [Card(5, Suits.S), Card(12, Suits.D)]
        test2.hand = [Card(5, Suits.S), Card(11, Suits.S)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _best_flush(test1, test2) == [test2]

    _test_best_flush_1()
    _test_best_flush_2()


def _test_kicker():
    from cards import Player, Table, Card, Suits, _kicker
    test1 = Player("Test1")
    table = Table()

    def _test_kicker_1():
        """
        Case when player has two cards, that don`t belong to combination
        """
        table.hand = [Card(5, Suits.D), Card(5, Suits.C), Card(12, Suits.H), Card(7, Suits.S), Card(12, Suits.C)]
        test1.hand = [Card(14, Suits.C), Card(11, Suits.S)]
        test1.hand_rank(table)

        assert _kicker(test1) == Card(14, Suits.C)

    def _test_kicker_2():
        """
        Case when player has one card, that don`t belong to combination
        """
        table.hand = [Card(5, Suits.D), Card(10, Suits.C), Card(12, Suits.H), Card(7, Suits.S), Card(12, Suits.C)]
        test1.hand = [Card(13, Suits.C), Card(10, Suits.S)]
        test1.hand_rank(table)

        assert _kicker(test1) == Card(13, Suits.C)

    _test_kicker_1()
    _test_kicker_2()


def _test_is_shared_kicker():
    from cards import Player, Table, Card, Suits, _is_shared_kicker
    test1 = Player("Test1")
    test2 = Player("Test2")
    table = Table()

    def _test_is_shared_kicker_1():
        """
        Case when table have two free cards
        """
        table.hand = [Card(5, Suits.D), Card(7, Suits.C), Card(12, Suits.H), Card(13, Suits.S), Card(12, Suits.C)]
        test1.hand = [Card(7, Suits.S), Card(3, Suits.D)]
        test2.hand = [Card(7, Suits.S), Card(3, Suits.S)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _is_shared_kicker(table, test1, test2) == Card(13, Suits.S)

    _test_is_shared_kicker_1()


def _test_pocket_card():
    from cards import Player, Table, Card, Suits, _pocket_card
    test1 = Player("Test1")
    test2 = Player("Test2")
    table = Table()

    def _test_pocket_card_1():
        """
        Case when players have same kickers
        """
        table.hand = [Card(7, Suits.H), Card(5, Suits.S), Card(2, Suits.H), Card(9, Suits.H), Card(7, Suits.C)]
        test1.hand = [Card(13, Suits.S), Card(12, Suits.D)]
        test2.hand = [Card(11, Suits.C), Card(13, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _pocket_card(test1) == Card(12, Suits.D)
        assert _pocket_card(test2) ==  Card(11, Suits.C)

    _test_pocket_card_1()


def _test_winner_when_combs_same():
    from cards import Player, Table, Card, Suits, _winner_when_combs_same
    test1 = Player("Test1")
    test2 = Player("Test2")
    table = Table()

    def _test_winner_when_combs_same_1():
        """
        Case when players have same kickers but diff pocket cards
        """
        table.hand = [Card(7, Suits.H), Card(5, Suits.S), Card(2, Suits.H), Card(9, Suits.H), Card(7, Suits.C)]
        test1.hand = [Card(13, Suits.S), Card(12, Suits.D)]
        test2.hand = [Card(11, Suits.C), Card(13, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _winner_when_combs_same(table, test1, test2) == [test1]

    def _test_winner_when_combs_same_2():
        """
        Case when players have same kickers
        """
        table.hand = [Card(7, Suits.H), Card(5, Suits.S), Card(2, Suits.H), Card(9, Suits.H), Card(7, Suits.C)]
        test1.hand = [Card(7, Suits.S), Card(12, Suits.D)]
        test2.hand = [Card(7, Suits.C), Card(13, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _winner_when_combs_same(table, test1, test2) == [test2]

    def _test_winner_when_combs_same_3():
        """
        Case when players have shared kicker
        """
        table.hand = [Card(3, Suits.H), Card(5, Suits.S), Card(6, Suits.H), Card(9, Suits.H), Card(8, Suits.C)]
        test1.hand = [Card(3, Suits.S), Card(4, Suits.D)]
        test2.hand = [Card(3, Suits.C), Card(4, Suits.H)]
        test1.hand_rank(table)
        test2.hand_rank(table)

        assert _winner_when_combs_same(table, test1, test2) == [test1, test2]

    _test_winner_when_combs_same_1()
    _test_winner_when_combs_same_2()
    _test_winner_when_combs_same_3()


if __name__ == '__main__':
    _test_best_straight()
    _test_best_flush()
    _test_kicker()
    _test_is_shared_kicker()
    _test_pocket_card()
