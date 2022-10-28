import random
import pandas
from tkinter import *
from os.path import exists
BACKGROUND_COLOR = "#B1DDC6"


def get_translation():
    canvas.itemconfig(card, image=back)
    canvas.itemconfig(language, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")
    window.after_cancel(timer)


def known_word():
    global data
    dictionary.remove(current_card)
    df = pandas.DataFrame.from_dict(dictionary)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_word()


def next_word():
    global current_card, timer
    current_card = random.choice(dictionary)
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(word, text=current_card["French"], fill="black")
    canvas.itemconfig(card, image=front)
    timer = window.after(3000, get_translation)


if __name__ == "__main__":
    # Retrieve data
    if exists("data/words_to_learn.csv"):
        data = pandas.read_csv("data/words_to_learn.csv")
    else:
        data = pandas.read_csv("data/french_words.csv")
    dictionary = data.to_dict(orient="records")
    current_card = dictionary[0]

    # Window
    window = Tk()
    window.title("Learn French with Flash Cards")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    # Flash Card
    canvas = Canvas(width=800, height=530, highlightthickness=0, bg=BACKGROUND_COLOR)
    front = PhotoImage(file="images/card_front.png")
    back = PhotoImage(file="images/card_back.png")
    card = canvas.create_image(400, 265, image=front)
    language = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
    word = canvas.create_text(400, 263, text=current_card["French"], font=("Ariel", 60, "bold"))
    canvas.grid(row=0, column=0, columnspan=2)

    # Buttons
    right = PhotoImage(file="images/right.png")
    wrong = PhotoImage(file="images/wrong.png")
    Button(image=right, bg=BACKGROUND_COLOR, borderwidth=0, command=known_word).grid(row=1, column=0, pady=15)
    Button(image=wrong, bg=BACKGROUND_COLOR, borderwidth=0, command=next_word).grid(row=1, column=1, pady=15)

    timer = window.after(3000, get_translation)


    window.mainloop()
