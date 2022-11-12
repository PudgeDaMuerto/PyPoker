import time
from gui import *
from cards import *
from tkinter import Tk

DEALER_INDEX = -3
S_BLIND_INDEX = -2
B_BLIND_INDEX = -1
btn_clicked = False

root = Tk()
gui = GUI(root)
gui.clear_table()
gui.hide_all_widgets()

players = [Player(f"Player {i + 1}") for i in range(5)]
players_queue = PlayersQueue([0, 1, 2, 3, 4])


def real_players(_players):
    return list(filter(lambda p: not p.is_fold, _players))


def raised_players(_players):
    return list(filter(lambda p: not p.is_raise, _players))


# Buttons commands
def on_call():
    _max_bet = max([_p.curr_bet for _p in players])

    player = players[gui.YOUR_PLAYER]
    player.bet(_max_bet - player.curr_bet)
    gui.set_bet(gui.YOUR_PLAYER, player.curr_bet)
    gui.hide_all_widgets()
    gui.set_money(player.money)

    global btn_clicked
    btn_clicked = True


def on_fold():
    player = players[gui.YOUR_PLAYER]
    player.is_fold = True
    gui.player_fold(gui.YOUR_PLAYER)
    gui.hide_all_widgets()

    global btn_clicked
    btn_clicked = True


def on_bet():
    if gui.bet_text.get():
        try:
            bet = int(gui.bet_text.get())
            _max_bet = max([_p.curr_bet for _p in players])

            if bet > _max_bet:
                player = players[gui.YOUR_PLAYER]
                player.bet(bet)
                player.is_raise = True

                gui.set_bet(gui.YOUR_PLAYER, player.curr_bet)
                gui.hide_all_widgets()
                gui.bet_text.delete(0, 'end')
                gui.set_money(player.money)

                global btn_clicked
                btn_clicked = True

            else:
                gui.show_message(f"You must bet more then {_max_bet}", 'red')
                gui.bet_text.delete(0, 'end')

        except ValueError:
            gui.show_message("Input integer value!", 'red')
            gui.bet_text.delete(0, 'end')
    else:
        gui.show_message("Input value of bet beyond the button!", 'red')


gui.btn_call.configure(command=on_call)
gui.btn_bet.configure(command=on_bet)
gui.btn_fold.configure(command=on_fold)

for i in range(5):
    gui.hide_player_hand(i)


def main():
    def is_end_of_turn(_players: list[Player]) -> bool:
        _real_players = real_players(_players)
        _max_bet = max([_p.curr_bet for _p in _real_players])

        for _p in _real_players:
            if _p.curr_bet != _max_bet:
                return False

        return True

    def calc_bank(_players: list[Player]) -> int:
        _bank = 0
        for _p in _players:
            _bank += _p.curr_bet

        return _bank

    def clear_bets(_players: list[Player]):
        for _p in _players:
            _p.curr_bet = 0

    import prolog as pl

    gui.give_role(players_queue.get_dealer(), "dealer")
    gui.give_role(players_queue.get_s_blind(), "small blind")
    gui.give_role(players_queue.get_b_blind(), "big blind")

    table = Table()
    deck = Deck()
    deck.shuffle()

    blind = 50
    # Preflop start

    pl.set_blind(blind)

    s_blind_player_index = players_queue.get_s_blind()
    b_blind_player_index = players_queue.get_b_blind()

    # First, make blinds
    gui.set_bet(s_blind_player_index, players[s_blind_player_index].bet(int(blind / 2)))
    gui.set_bet(b_blind_player_index, players[b_blind_player_index].bet(blind))

    # Give cards for players and set your player rank
    for p_index in players_queue:
        player = players[p_index]

        player.draw(deck, 2)
        gui.set_player_hand(p_index, player.hand)
        player.hand_rank(table)

    gui.set_rank(players[gui.YOUR_PLAYER].rank.name)
    gui.show_players_hand([gui.YOUR_PLAYER])

    is_raised = False
    end = False
    # Start cycle for preflop
    while not end:
        global btn_clicked
        btn_clicked = False
        for p_index in players_queue:
            print(p_index)
            gui.show_message(f"{p_index}", color='black')
            max_bet = max([p.curr_bet for p in players])

            player = players[p_index]
            if player.is_fold:
                continue

            gui.start_player_turn(p_index)

            if p_index != gui.YOUR_PLAYER:
                time.sleep(1)
                if max_bet > blind:
                    if pl.preflop_call_more(player.hand, max_bet):
                        player.bet(max_bet - player.curr_bet)
                        gui.set_bet(p_index, player.curr_bet)
                        # gui.end_player_turn(p_index)
                    else:
                        # players_queue.remove(p_index)
                        player.is_fold = True
                        gui.player_fold(p_index)
                        print(f"{p_index}: fold")
                        gui.show_message(f"{players_queue}", 'black')
                        # ui.end_player_turn(p_index)
                else:
                    if bet := pl.preflop_raise(player.hand) and not is_raised:
                        player.bet(bet)
                        gui.set_bet(p_index, player.curr_bet)
                        is_raised = True
                        # gui.end_player_turn(p_index)
                    else:
                        player.bet(max_bet - player.curr_bet)
                        gui.set_bet(p_index, player.curr_bet)
                        # gui.end_player_turn(p_index)

            else:
                gui.show_all_widgets()
                while not btn_clicked:
                    pass
                print("click")

            time.sleep(1)
            gui.end_player_turn(p_index)
            end = is_end_of_turn(players)
            if end:
                print('end')
                break

    gui.clear_bets()
    gui.set_bank(calc_bank(players))
    clear_bets(players)

    table.draw(deck, 3)
    for p in players:
        p.hand_rank(table)

    gui.set_table_cards(*table.hand, places=(0, 1, 2))

    gui.set_rank(players[2].rank.name)

    time.sleep(3)


    # for i in range(3, 5):
    #     table.draw(deck, 1)
    #     gui.set_table_card(table.hand[-1], i)
    #     gui.set_rank(players[2].rank.name)
    #     time.sleep(5)
    #     for p in players_queue.list:
    #         p.hand_rank(table)

    winners = rank_comparison(table, *players)
    gui.show_message(f'WIN - {winners} with {winners[0].rank.name}', 'black')

    winners_indexes = []
    for i in winners:
        winners_indexes.append(players.index(i))

    gui.show_players_hand(winners_indexes)


gui.start(main)
gui.start_mainloop()

