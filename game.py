import time
from gui import *
from cards import *
from tkinter import Tk
from tkinter import messagebox
from save import Save

DEALER_INDEX = -3
S_BLIND_INDEX = -2
B_BLIND_INDEX = -1

btn_clicked = False

save = Save()
root = Tk()
gui = GUI(root)


def create_players():
    _players = [Player(f"Player {_i + 1}") for _i in range(5)]
    _players_queue = PlayersQueue([0, 1, 2, 3, 4])

    return _players, _players_queue


if save.get_data():
    players, players_queue = save.get_data()
    for p in players:
        p.rank = None
        p.comb = None
        p.curr_bet = 0
        p.is_fold = False
        p.is_raise = False
else:
    players, players_queue = create_players()


gui.clear_table()
gui.set_money(players[GUI.YOUR_PLAYER].money)
gui.hide_all_widgets()
for i in range(5):
    gui.hide_player_hand(i)


def on_closing():
    if messagebox.askokcancel("Save", "Do you want to save game?"):
        save.save_data(players, players_queue)
        time.sleep(3)
        root.destroy()
    else:
        root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)


def real_players(_players):
    return list(filter(lambda _p: not _p.is_fold and not _p.is_lose, _players))


def raised_players(_players):
    return list(filter(lambda _p: not _p.is_raise, _players))


def is_end_of_turn(_players: list[Player]) -> bool:
    _real_players = real_players(_players)
    _real_players_with_money = list(filter(lambda _p: _p.money > 0, _real_players))
    _max_bet = max([_p.curr_bet for _p in _real_players])

    for _p in _real_players_with_money:
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


def on_check():
    gui.hide_all_widgets()
    global btn_clicked
    btn_clicked = True


gui.btn_call.configure(command=on_call)
gui.btn_bet.configure(command=on_bet)
gui.btn_fold.configure(command=on_fold)
gui.btn_check.configure(command=on_check)


def game():
    from prolog import Pl, State
    pl = Pl()
    blind = 50
    bank = 0

    def _start_state(state: State, _bank: int):
        for _p in players:
            _p.hand_rank(table)

        gui.set_rank(players[gui.YOUR_PLAYER].rank)

        _is_raised = False
        _end = False
        _first_turn = True
        while not _end:
            global btn_clicked
            btn_clicked = False
            for _p_index in players_queue:
                _player = players[_p_index]
                if _player.is_fold or _player.is_lose:
                    continue

                _max_bet = max([_p.curr_bet for _p in players])

                gui.start_player_turn(_p_index)

                if _p_index != gui.YOUR_PLAYER:
                    time.sleep(1)
                    if _max_bet > 0:
                        if pl.state_call_more(_player.hand, _player.rank, _max_bet, state):
                            _player.bet(_max_bet - _player.curr_bet)
                            gui.set_bet(_p_index, _player.curr_bet)
                            if (_bet := pl.state_raise(_player.rank, state)) and not _is_raised:
                                _player.bet(_bet)
                                gui.set_bet(_p_index, _player.curr_bet)
                                _is_raised = True
                        else:
                            _player.is_fold = True
                            gui.player_fold(_p_index)
                    else:
                        if (_bet := pl.state_raise(_player.rank, state)) and not _is_raised:
                            _player.bet(_bet)
                            gui.set_bet(_p_index, _player.curr_bet)
                            _is_raised = True
                        else:
                            _player.bet(_max_bet - _player.curr_bet)
                            gui.set_bet(_p_index, _player.curr_bet)

                elif len(real_players(players)) != 1:
                    gui.show_all_widgets()
                    disable_button(gui.btn_call) if _max_bet == 0 else disable_button(gui.btn_check)
                    while not btn_clicked:
                        pass

                time.sleep(1)
                gui.end_player_turn(_p_index)
                if len(real_players(players)) == 1:
                    _end = True
                    break

                _end = is_end_of_turn(players)

                if _end and not _first_turn:
                    break

            _first_turn = False

        gui.clear_bets()
        _bank += calc_bank(players)
        gui.set_bank(_bank)
        clear_bets(players)

        return _bank

    def _start_preflop(_bank: int):
        # Give cards for players and set your player rank
        for _p_index in players_queue:
            _player = players[_p_index]

            _player.draw(deck, 2)
            gui.set_player_hand(_p_index, _player.hand)
            _player.hand_rank(table)

        if not players[gui.YOUR_PLAYER].is_lose:
            gui.set_rank(players[gui.YOUR_PLAYER].rank)
            gui.show_players_hand([gui.YOUR_PLAYER])

        _is_raised = False
        _end = False
        _first_turn = True
        # Start cycle for Preflop
        while not _end:
            global btn_clicked
            btn_clicked = False
            for _p_index in players_queue:
                _player = players[_p_index]
                if _player.is_fold or _player.is_lose:
                    continue

                _max_bet = max([_p.curr_bet for _p in players])

                gui.start_player_turn(_p_index)

                if _p_index != gui.YOUR_PLAYER:
                    time.sleep(1)
                    if _max_bet > blind:
                        if pl.preflop_call_more(_player.hand, _max_bet):
                            _player.bet(_max_bet - _player.curr_bet)
                            gui.set_bet(_p_index, _player.curr_bet)
                        else:
                            _player.is_fold = True
                            gui.player_fold(_p_index)
                    else:
                        if (bet := pl.preflop_raise(_player.hand)) and not _is_raised:
                            _player.bet(bet)
                            gui.set_bet(_p_index, _player.curr_bet)
                            _is_raised = True
                        else:
                            _player.bet(_max_bet - _player.curr_bet)
                            gui.set_bet(_p_index, _player.curr_bet)

                elif len(real_players(players)) != 1:
                    gui.show_all_widgets()
                    disable_button(gui.btn_check) if _max_bet > 0 else disable_button(gui.btn_call)
                    while not btn_clicked:
                        pass

                time.sleep(1)
                gui.end_player_turn(_p_index)

                if len(real_players(players)) == 1:
                    _end = True
                    break

                _end = is_end_of_turn(players)
                if _end and not _first_turn:
                    break

            _first_turn = False

        gui.clear_bets()
        _bank += calc_bank(players)
        gui.set_bank(_bank)
        clear_bets(players)

        return _bank

    gui.set_bank(0)
    gui.clear_table()
    gui.hide_all_widgets()
    for i in range(5):
        gui.hide_player_hand(i)
        gui.clear_role(i)
    for p in players:
        p.clear()
        p.is_fold = False

    gui.reset_players_colors(players_queue)

    for i in range(5):
        if players[i].is_lose:
            gui.player_lose(i)

    gui.give_role(players_queue.get_dealer(), "dealer")
    gui.give_role(players_queue.get_s_blind(), "small blind")
    gui.give_role(players_queue.get_b_blind(), "big blind")

    table = Table()
    deck = Deck()
    deck.shuffle()

    # Preflop start

    pl.set_blind(blind)

    s_blind_player_index = players_queue.get_s_blind()
    b_blind_player_index = players_queue.get_b_blind()

    # First, make blinds

    gui.set_bet(s_blind_player_index, players[s_blind_player_index].bet(int(blind / 2)))
    gui.set_bet(b_blind_player_index, players[b_blind_player_index].bet(blind))

    bank = _start_preflop(bank)

    time.sleep(2)
    table.draw(deck, 3)
    gui.set_table_cards(*table.hand, places=(0, 1, 2))
    bank = _start_state(State.FLOP, bank)

    time.sleep(2)
    table.draw(deck, 1)
    gui.set_table_cards(table.hand[-1], places=(3,))
    bank = _start_state(State.TURN, bank)

    time.sleep(2)
    table.draw(deck, 1)
    gui.set_table_cards(table.hand[-1], places=(4,))
    bank = _start_state(State.RIVER, bank)

    winners = rank_comparison(table, *real_players(players))
    gui.show_message(f'WIN - {", ".join([str(_p) for _p in winners])} with {winners[0].rank}', 'black')

    money_won = int(bank / len(winners))

    winners_indexes = []
    for winner in winners:
        winners_indexes.append(players.index(winner))
        winner.money += money_won

    gui.set_money(players[gui.YOUR_PLAYER].money)
    # gui.show_players_hand(winners_indexes)
    gui.show_players_hand(players_queue)

    players_queue.l_move()

    for p_index in players_queue:
        if players[p_index].money <= 0:
            gui.player_lose(p_index)
            players_queue.remove(p_index)
            players[p_index].is_lose = True
            if p_index == GUI.YOUR_PLAYER:
                save.delete_data()
                gui.game_over()

    time.sleep(10)


def main():
    while True:
        game()


gui.start(main)
gui.start_mainloop()
