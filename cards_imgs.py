from PIL import Image, ImageTk


def create_imgs(resize: int | float):
    cards_imgs = dict()

    for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
        for rank in range(2, 15):
            img = Image.open(f'static/cards_imgs/{rank}_of_{suit}.png')
            img = img.resize((int(img.width/resize), int(img.height/resize)))
            cards_imgs[f'{rank} of {suit}'] = ImageTk.PhotoImage(img)

    return cards_imgs
