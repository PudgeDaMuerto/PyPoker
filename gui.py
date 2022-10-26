import tkinter
from tkinter import *
from cards_imgs import create_imgs


class GUI:
    SIZE_X = 1280
    SIZE_Y = 720
    FRAME_SIZE = 80
    BLUE = '#33FFFF'
    GREEN = '#00FF00'

    def __init__(self):
        self.window = Tk()
        self.window.title("Poker")
        self.window.geometry(f"{GUI.SIZE_X}x{GUI.SIZE_Y}")
        self.window.resizable(width=False, height=False)
        self.window.configure(background="green")

        # Create images for cards
        self.table_cards = create_imgs(5.5)
        self.hand_cards = create_imgs(10)

        # Create labels for players and place they
        self.player_labels = [Label(self.window, text=f"Player {i + 1}") for i in range(5)]

        self.player_labels[0].place(x=GUI.SIZE_X - 350, y=20, anchor="e")
        self.player_labels[1].place(x=GUI.SIZE_X - 20, y=350, anchor="e")
        self.player_labels[2].place(x=GUI.SIZE_X / 2 - 20, y=GUI.SIZE_Y - 20, anchor="s")
        self.player_labels[3].place(x=20, y=350)
        self.player_labels[4].place(x=350, y=20)

        self.player_labels[2].configure(text="YOU")

        self.your_money_label = Label(self.window, text="Your money:")
        self.your_money_label.place(x=20, y=GUI.SIZE_Y - 10, anchor='sw')
        self.money_label = Label(self.window, text="5000")
        self.money_label.place(x=100, y=GUI.SIZE_Y - 10, anchor='sw')

        self.combination_label = Label(self.window, text="High Card")
        self.combination_label.place(x=300, y=GUI.SIZE_Y - 10, anchor='sw')

        self.btn_check = Button(text="Check", width=10, height=2, bg=GUI.BLUE, state='disabled')
        self.btn_call = Button(text="Call", width=10, height=2, bg=GUI.GREEN, state='disabled')
        self.btn_fold = Button(text="Fold", width=10, height=2, bg='red', state='disabled')
        self.btn_bet = Button(text="Bet", width=10, height=2, bg='yellow', state='disabled')

        self.btn_fold.place(x=GUI.SIZE_X / 2 - 200, y=GUI.SIZE_Y - 170)
        self.btn_check.place(x=GUI.SIZE_X / 2 - 110, y=GUI.SIZE_Y - 170)
        self.btn_call.place(x=GUI.SIZE_X / 2 - 20, y=GUI.SIZE_Y - 170)
        self.btn_bet.place(x=GUI.SIZE_X / 2 + 70, y=GUI.SIZE_Y - 170)

        self.bet_text = Entry(self.window, width=13)
        self.bet_text.place(x=GUI.SIZE_X / 2 + 70, y=GUI.SIZE_Y - 125)

        # Create labels for cards on table and place they
        self.table_cards_labels = [Label(self.window, image=self.table_cards['14 of spades'], bg='green') for _ in range(5)]

        self.table_cards_labels[0].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 - 200, anchor='center')
        self.table_cards_labels[1].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 - 100, anchor='center')
        self.table_cards_labels[2].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2, anchor='center')
        self.table_cards_labels[3].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 + 100, anchor='center')
        self.table_cards_labels[4].place(y=GUI.SIZE_Y / 2, x=GUI.SIZE_X / 2 + 200, anchor='center')

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


def hide_widgets(*buttons: tkinter.Widget):
    for button in buttons:
        old_place = button.place_info()
        button.place_configure(x=int(old_place['x']) + 1000)


def show_widgets(*buttons: tkinter.Widget):
    for button in buttons:
        old_place = button.place_info()
        button.place_configure(x=int(old_place['x']) - 1000)
