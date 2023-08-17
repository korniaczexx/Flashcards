from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
data = None
timer = None

try:
    data = pd.read_csv(".//data//to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv(".//data//french_words.csv")

word = random.choice(data['French'])

def new_word():
    global word
    word = random.choice(data['French'])
    count_down(3)
    language_label.config(text='French', bg='white')
    word_label.config(text=word, bg='white')
    card_front.itemconfig(canvas_image, image=image_png_front)

def around():
    card_front.itemconfig(canvas_image, image=image_png_back)
    language_label.config(text='English', bg='#94c3ab')
    french_word = word_label.cget('text')
    try:
        english_word = data.loc[data['French'] == french_word, 'English'].values[0]
        word_label.config(text=english_word, bg='#94c3ab')
    except IndexError:
        print(f"The word {french_word} has no translation in the file")

def count_down(count):
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        around()

def known_word():
    french_word = word_label.cget('text')
    data.drop(data[data['French'] == french_word].index, inplace=True)
    data.to_csv(".//data//to_learn.csv", index=False)
    new_word()

window = Tk()
window.config(bg=BACKGROUND_COLOR)
window.title("Flashy")
window.config(pady=50, padx=50)

card_front = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
image_png_front = PhotoImage(file=".\images\card_front.png")
image_png_back = PhotoImage(file=".\images\card_back.png")

canvas_image = card_front.create_image(400, 263, image=image_png_front)
card_front.grid(column=0, row=0, padx=50, pady=50, columnspan=2)

known_image = PhotoImage(file=".//images//right.png")
unknown_image = PhotoImage(file=".\images\wrong.png")

known_button = Button(image=known_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=known_word)
known_button.grid(column=0, row=1)
unknown_button = Button(image=unknown_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=new_word)
unknown_button.grid(column=1, row=1)

language_label = Label(text="French", font=("Ariel", 40, "italic"), bg='white')
word_label = Label(text=word, font=("Ariel", 60, "bold"), bg='white')

card_front.create_window(400, 150, window=language_label)
card_front.create_window(400, 263, window=word_label)
count_down(3)

window.mainloop()
