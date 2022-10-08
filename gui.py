from tkinter import *
from cards_imgs import create_imgs


SIZE_X = 1280
SIZE_Y = 720
FRAME_SIZE = 80
BLUE = '#33FFFF'
GREEN = '#00FF00'

window = Tk()
window.title("Poker")
window.geometry(f"{SIZE_X}x{SIZE_Y}")
window.resizable(width=False, height=False)
window.configure(background="green")

# Create images for cards
table_cards = create_imgs(5.5)
hand_cards = create_imgs(10)

# Create labels for players and place they
player_labels = [Label(window, text=f"Player {i + 1}") for i in range(5)]

player_labels[0].place(x=SIZE_X - 350, y=20, anchor="e")
player_labels[1].place(x=SIZE_X - 20, y=350, anchor="e")
player_labels[2].place(x=SIZE_X / 2 - 20, y=SIZE_Y - 20, anchor="s")
player_labels[3].place(x=20, y=350)
player_labels[4].place(x=350, y=20)

player_labels[2].configure(text="YOU")

your_money_label = Label(window, text="Your money:")
your_money_label.place(x=20, y=SIZE_Y - 10, anchor='sw')
money_label = Label(window, text="5000")
money_label.place(x=100, y=SIZE_Y - 10, anchor='sw')

combination_label = Label(window, text="High Card")
combination_label.place(x=300, y=SIZE_Y - 10, anchor='sw')


btn_check = Button(text="Check", width=10, height=2, bg=BLUE, state='disabled')
btn_call = Button(text="Call", width=10, height=2, bg=GREEN, state='disabled')
btn_fold = Button(text="Fold", width=10, height=2, bg='red', state='disabled')
btn_bet = Button(text="Bet", width=10, height=2, bg='yellow', state='disabled')

btn_fold.place(x=SIZE_X / 2 - 200, y=SIZE_Y - 170)
btn_check.place(x=SIZE_X / 2 - 110, y=SIZE_Y - 170)
btn_call.place(x=SIZE_X / 2 - 20, y=SIZE_Y - 170)
btn_bet.place(x=SIZE_X / 2 + 70, y=SIZE_Y - 170)

bet_text = Entry(window, width=13)
bet_text.place(x=SIZE_X / 2 + 70, y=SIZE_Y - 125)

# Create labels for cards on table and place they
table_cards_labels = [Label(window, image=table_cards['14 of spades'], bg='green') for _ in range(5)]

table_cards_labels[0].place(y=SIZE_Y / 2, x=SIZE_X / 2 - 200, anchor='center')
table_cards_labels[1].place(y=SIZE_Y / 2, x=SIZE_X / 2 - 100, anchor='center')
table_cards_labels[2].place(y=SIZE_Y / 2, x=SIZE_X / 2, anchor='center')
table_cards_labels[3].place(y=SIZE_Y / 2, x=SIZE_X / 2 + 100, anchor='center')
table_cards_labels[4].place(y=SIZE_Y / 2, x=SIZE_X / 2 + 200, anchor='center')


players_cards = list()
hand_cards_labels = [Label(window, image=hand_cards['2 of spades'], bg='green') for _ in range(10)]

hand_cards_labels[0].place(x=SIZE_X - 400, y=40, anchor="n")
hand_cards_labels[1].place(x=SIZE_X - 345, y=40, anchor="n")
players_cards.append([hand_cards_labels[0], hand_cards_labels[1]])

hand_cards_labels[2].place(x=SIZE_X - 20 - 50 - 15, y=350 + 20, anchor="n")
hand_cards_labels[3].place(x=SIZE_X - 20 + 5 - 15, y=350 + 20, anchor="n")
players_cards.append([hand_cards_labels[2], hand_cards_labels[3]])

hand_cards_labels[4].place(x=SIZE_X / 2 - 50, y=SIZE_Y - 20 - 30, anchor="s")
hand_cards_labels[5].place(x=SIZE_X / 2 + 5, y=SIZE_Y - 20 - 30, anchor="s")
players_cards.append([hand_cards_labels[4], hand_cards_labels[5]])

hand_cards_labels[6].place(x=20 + 10, y=350 + 30, anchor="n")
hand_cards_labels[7].place(x=20 + 65, y=350 + 30, anchor="n")
players_cards.append([hand_cards_labels[6], hand_cards_labels[7]])

hand_cards_labels[8].place(x=345, y=20 + 30, anchor="n")
hand_cards_labels[9].place(x=345 + 55, y=20 + 30, anchor="n")
players_cards.append([hand_cards_labels[8], hand_cards_labels[9]])

# player_labels[2]['text'] += 'dealer'
# table_cards_labels[2]['bg'] = 'red'


def start_mainloop():
    window.mainloop()
