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
gui.set_rank(players_queue.list[2].rank.name)


ranks = []
for i in range(3, 5):
    table.draw(deck, 1)
    for p in players_queue.list:
        p.hand_rank(table)
    ranks.append(players_queue.list[2].rank.name)

winners = rank_comparison(table, *players)

gui.delay(2, lambda: gui.set_table_card(table.hand[-2], 3))
gui.delay(4, lambda: gui.set_table_card(table.hand[-1], 4))

gui.delay(2, lambda: gui.set_rank(ranks[0]))
gui.delay(4, lambda: gui.set_rank(ranks[1]))

gui.delay(6, lambda: gui.show_message(f'WIN - {winners} with {winners[0].rank.name}', 'black'))

winners_indexes = []
for i in winners:
    winners_indexes.append(players.index(i))

gui.delay(6, lambda: gui.show_players_hand(winners_indexes))

gui.start_mainloop()
