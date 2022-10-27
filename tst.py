cards_val = [2, 3, 4, 5, 6, 6, 6]

from cards import Queue, Player, PlayersQueue

players = [Player(f'player {i + 1}') for i in range(5)]

queue = PlayersQueue(players)

print(queue)

print('dealer:', queue.get_dealer())
print('small blind:', queue.get_s_blind())
print('big blind:', queue.get_b_blind())

