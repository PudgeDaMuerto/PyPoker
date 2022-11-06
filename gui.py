import threading
import tkinter
from tkinter import *

from cards_imgs import create_imgs


class GUI:
    SIZE_X = 1280
    SIZE_Y = 720
    FRAME_SIZE = 80
    BLUE = '#33FFFF'
    GREEN = '#00FF00'
    YOUR_PLAYER = 2
    MESSAGE_SECONDS = 3

    def __init__(self, root):
        self.window: tkinter.Tk = root
        self.window.title("Poker")
        self.window.geometry(f"{GUI.SIZE_X}x{GUI.SIZE_Y}+10+10")
        self.window.resizable(width=False, height=False)
        self.window.configure(background="green")

        # Create images for cards
        self.table_cards = create_imgs(5.5)
        self.hand_cards = create_imgs(10)

        # Create labels for players and place them
        self.player_labels = [Label(self.window, text=f"Player {i + 1}") for i in range(5)]

        self.player_labels[0].place(x=GUI.SIZE_X - 350, y=20, anchor="e")
        self.player_labels[1].place(x=GUI.SIZE_X - 20, y=350, anchor="e")
        self.player_labels[GUI.YOUR_PLAYER].place(x=GUI.SIZE_X / 2 - 20, y=GUI.SIZE_Y - 20, anchor="s")
        self.player_labels[3].place(x=20, y=350)
        self.player_labels[4].place(x=350, y=20)

        self.player_labels[GUI.YOUR_PLAYER].configure(text="YOU")

        # Create labels for players bets
        self.players_bets_labels = [Label(self.window, text='0', bg='green') for _ in range(5)]
        self.players_bets_labels[0].place(x=GUI.SIZE_X - 350 + 10, y=20, anchor="w")
        self.players_bets_labels[1].place(x=GUI.SIZE_X - 20 - 55, y=350, anchor="e")
        self.players_bets_labels[GUI.YOUR_PLAYER].place(x=GUI.SIZE_X / 2 - 20 + 25, y=GUI.SIZE_Y - 20, anchor="sw")
        self.players_bets_labels[3].place(x=20 + 55, y=350, anchor="nw")
        self.players_bets_labels[4].place(x=350 + 55, y=20, anchor="nw")

        # Create money label
        self.your_money_label = Label(self.window, text="Your money:")
        self.your_money_label.place(x=20, y=GUI.SIZE_Y - 10, anchor='sw')
        self.money_label = Label(self.window, text="1000")
        self.money_label.place(x=100, y=GUI.SIZE_Y - 10, anchor='sw')

        # Create combination label
        self.combination_label = Label(self.window, text="High Card")
        self.combination_label.place(x=300, y=GUI.SIZE_Y - 10, anchor='sw')

        # Create bank label and place it
        self.bank_label = Label(self.window, text='Bank', width=10)
        self.bank_label.place(x=GUI.SIZE_X/2, y=200, anchor='n')
        self.bank_sum_label = Label(self.window, text='0', width=10)
        self.bank_sum_label.place(x=GUI.SIZE_X/2, y=225, anchor='n')

        # Create and place buttons for player
        self.btn_check = Button(text="Check", width=10, height=2, bg=GUI.BLUE)
        self.btn_call = Button(text="Call", width=10, height=2, bg=GUI.GREEN)
        self.btn_fold = Button(text="Fold", width=10, height=2, bg='red')
        self.btn_bet = Button(text="Bet", width=10, height=2, bg='yellow')

        self.btn_fold.place(x=GUI.SIZE_X / 2 - 200, y=GUI.SIZE_Y - 170)
        self.btn_check.place(x=GUI.SIZE_X / 2 - 110, y=GUI.SIZE_Y - 170)
        self.btn_call.place(x=GUI.SIZE_X / 2 - 20, y=GUI.SIZE_Y - 170)
        self.btn_bet.place(x=GUI.SIZE_X / 2 + 70, y=GUI.SIZE_Y - 170)

        self.bet_text = Entry(self.window, width=13)
        self.bet_text.place(x=GUI.SIZE_X / 2 + 70, y=GUI.SIZE_Y - 125)

        # Create labels for cards on table and place them
        self.table_cards_labels = [Label(self.window, image=self.table_cards['14 of spades'], bg='green') for _ in range(5)]

        self.table_cards_labels[0].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 - 200, anchor='center')
        self.table_cards_labels[1].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 - 100, anchor='center')
        self.table_cards_labels[2].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2, anchor='center')
        self.table_cards_labels[3].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 + 100, anchor='center')
        self.table_cards_labels[4].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 + 200, anchor='center')

        # Create players hands, placing them, and save in list
        self.players_cards = list()
        self.hand_cards_labels = [Label(self.window, image=self.hand_cards['2 of spades'], bg='green') for _ in range(10)]

        self.hand_cards_labels[0].place(x=GUI.SIZE_X - 400, y=40, anchor="n")
        self.hand_cards_labels[1].place(x=GUI.SIZE_X - 345, y=40, anchor="n")
        self.players_cards.append([self.hand_cards_labels[0], self.hand_cards_labels[1]])

        self.hand_cards_labels[2].place(x=GUI.SIZE_X - 20 - 50 - 15, y=350 + 20, anchor="n")
        self.hand_cards_labels[3].place(x=GUI.SIZE_X - 20 + 5 - 15, y=350 + 20, anchor="n")
        self.players_cards.append([self.hand_cards_labels[2], self.hand_cards_labels[3]])

        self.hand_cards_labels[4].place(x=GUI.SIZE_X / 2 - 50, y=GUI.SIZE_Y - 20 - 30, anchor="s")
        self.hand_cards_labels[5].place(x=GUI.SIZE_X / 2 + 5, y=GUI.SIZE_Y - 20 - 30, anchor="s")
        self.players_cards.append([self.hand_cards_labels[4], self.hand_cards_labels[5]])

        self.hand_cards_labels[6].place(x=20 + 10, y=350 + 30, anchor="n")
        self.hand_cards_labels[7].place(x=20 + 65, y=350 + 30, anchor="n")
        self.players_cards.append([self.hand_cards_labels[6], self.hand_cards_labels[7]])

        self.hand_cards_labels[8].place(x=345, y=20 + 30, anchor="n")
        self.hand_cards_labels[9].place(x=345 + 55, y=20 + 30, anchor="n")
        self.players_cards.append([self.hand_cards_labels[8], self.hand_cards_labels[9]])

        # self.player_labels[2]['text'] += 'dealer'
        # self.table_cards_labels[2]['bg'] = 'red'

    def start_mainloop(self):
        self.window.mainloop()

    def hide_all_widgets(self):
        hide_widgets(self.btn_bet, self.bet_text, self.btn_call, self.btn_check, self.btn_fold)

    def show_all_widgets(self):
        show_widgets(self.btn_bet, self.bet_text, self.btn_call, self.btn_check, self.btn_fold)

    def hide_player_hand(self, player_index):
        hide_widgets(*self.players_cards[player_index])

    def show_players_hand(self, player_indexes: list[int]):
        for p in player_indexes:
            show_widgets(*self.players_cards[p])

    def set_player_hand(self, player_index, cards: list):
        for i in range(len(cards)):
            self.players_cards[player_index][i]['image'] = self.hand_cards[str(cards[i])]

    def set_table_cards(self, *cards: str, places: tuple):
        assert len(cards) == len(places), "Not enough places or cards!"
        for place, card in zip(places, cards):
             self.table_cards_labels[place]['image'] = self.table_cards[str(card)]

    def set_table_card(self, card: str, place: int):
        self.table_cards_labels[place]['image'] = self.table_cards[str(card)]

    def clear_table(self):
        for card in self.table_cards_labels:
            card['image'] = ''

    def show_message(self, text: str, color: str):
        message_label = Label(self.window, text=text, fg=color)
        message_label.pack(anchor='nw')
        message_label.after(GUI.MESSAGE_SECONDS * 1000, lambda: message_label.destroy())

    def set_rank(self, rank: str):
        self.combination_label['text'] = rank

    def refresh(self):
        pos_x = self.window.winfo_x()
        pos_y = self.window.winfo_y()
        self.window.update()
        self.window.geometry(f'+{pos_x}+{pos_y}')
        self.window.after(1000, self.refresh)

    def start(self, func):
        self.refresh()
        threading.Thread(target=func).start()


hidden_widgets = []


def hide_widgets(*buttons: tkinter.Widget):
    for button in buttons:
        if button not in hidden_widgets:
            old_place = button.place_info()
            button.place_configure(x=int(old_place['x']) + 10000)
            hidden_widgets.append(button)


def show_widgets(*buttons: tkinter.Widget):
    for button in buttons:
        if button in hidden_widgets:
            old_place = button.place_info()
            button.place_configure(x=int(old_place['x']) - 10000)
            hidden_widgets.remove(button)
