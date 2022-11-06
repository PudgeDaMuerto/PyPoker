import time
from gui import *
from cards import *
from tkinter import Tk

DEALER_INDEX = -3
S_BLIND_INDEX = -2
B_BLIND_INDEX = -1

root = Tk()
gui = GUI(root)
gui.clear_table()


for i in range(5):
    gui.hide_player_hand(i)


def a_main():
    players = [Player(f"Player {i + 1}") for i in range(5)]
    players_queue = PlayersQueue(players)

    table = Table()
    deck = Deck()

    deck.shuffle()
    table.draw(deck, 3)
    gui.set_table_cards(*table.hand, places=(0, 1, 2))

    for i, p in enumerate(players_queue.list):
        p.draw(deck, 2)
        gui.set_player_hand(i, p.hand)
        p.hand_rank(table)

    gui.show_players_hand([2])
    gui.set_rank(players[2].rank.name)

    time.sleep(5)
    for i in range(3, 5):
        table.draw(deck, 1)
        gui.set_table_card(table.hand[-1], i)
        gui.set_rank(players[2].rank.name)
        time.sleep(5)
        for p in players_queue.list:
            p.hand_rank(table)

    winners = rank_comparison(table, *players)

    gui.show_message(f'WIN - {winners} with {winners[0].rank.name}', 'black')

    winners_indexes = []
    for i in winners:
        winners_indexes.append(players.index(i))

    gui.show_players_hand(winners_indexes)


gui.start(a_main)
gui.start_mainloop()

