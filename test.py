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


if __name__ == '__main__':
    _test_best_straight()
    _test_best_flush()
