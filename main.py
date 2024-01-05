from tkinter import *
import random
import math

FONT_NAME = "Verdana"
BLUE = "steel blue"
WHITE = "white smoke"
RED = "tomato"
num_words = 0
num_mistakes = 0
timer = None

# ----- create word list --------
with open("words.txt", "r") as file:
    data = file.readlines()
stripped_data = [word.strip("\n") for word in data]
word_list = [word for word in stripped_data if len(word) > 3]

# random.shuffle(word_list) OR
random_list = [random.choice(word_list) for n in range(0, 200)]
random_text = ""
for word in random_list[:55]:
    random_text += word + " "


def reset():
    global num_words, num_mistakes, timer, random_text
    display.delete(1.0, END)
    random_text = ""
    num_words = 0
    num_mistakes = 0
    type_box.delete(1.0, END)
    type_box.bind("<Key>", func=start_test)
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"Press Start: ")
    for word in random_list[56:110]:
        random_text += word + " "
    display.insert(index=END, chars=random_text)
    instructions.config(text="Type the words shown as quickly as you can.\nSeparate words with a space.", font=(FONT_NAME, 16, "normal"), fg=WHITE)


def give_results():
    global num_words, num_mistakes
    user_input = type_box.get(1.0, END)
    user_words = user_input.split()
    given_words = display.get(1.0, END)
    given_list = given_words.split()
    for n in range(len(user_words)):
        num_words += 1
        if user_words[n] != given_list[n]:
            num_mistakes += 1
    corrected_wpm = (num_words - num_mistakes) * 2
    canvas.itemconfig(timer_text, text=f"Your speed: {corrected_wpm} WPM", fill=RED)
    instructions.config(text="STOP", fg=RED, font=(FONT_NAME, 24, "bold"))


def start_timer(count):
    global timer, timer_on
    count_minute = math.floor(count / 60)
    count_seconds = count % 60
    if count_seconds < 10:
        count_seconds = "0" + str(count_seconds)

    canvas.itemconfig(timer_text, text=f"Time left: {count_minute}:{count_seconds}")
    if count > 0:
        timer = window.after(1000, start_timer, count-1)
    elif count == 0:
        give_results()


def start_test(event):
    type_box.unbind("<Key>")
    count = 0.5 * 60
    start_timer(count)


# -------- UI ------------
window = Tk()
window.title("Typing Speed Test")
window.config(padx=50, pady=20, background=BLUE)
window.minsize(width=600, height=600)

title = Label(text="Test Your Typing Speed", bg=BLUE, fg=WHITE, font=(FONT_NAME, 40, "normal"))
title.config(padx=20, pady=20)
title.grid(column=0, row=0, columnspan=2)

instructions = Label(text="Type the words shown as quickly as you can.\nSeparate words with a space.", font=(FONT_NAME, 16, "normal"), fg=WHITE, bg=BLUE)
instructions.config(padx=10, pady=20)
instructions.grid(column=0, row=1, columnspan=2)

display = Text(width=35, height=9, font=(FONT_NAME, 16, "normal"), bg=WHITE, spacing2=2, wrap=WORD)
display.config(padx=10, pady=5)
display.grid(column=0, row=2, pady=10, columnspan=2)
display.insert(index=END, chars=random_text)

type_box = Text(width=35, height=3, font=(FONT_NAME, 16, "normal"), bg=WHITE, wrap=WORD)
type_box.config(padx=10, pady=10)
type_box.focus()
type_box.bind("<Key>", func=start_test)
type_box.grid(column=0, row=3, pady=10, columnspan=2)

canvas = Canvas(width=300, height=35, bg=BLUE, highlightthickness=0)
timer_text = canvas.create_text(140, 15, text="Type to begin timer.", fill=WHITE, font=(FONT_NAME, 24, "bold"))
canvas.grid(column=0, row=4, columnspan=2, pady=10)

# reset_canvas = Canvas(width=235, height=35, bg=BLUE, highlightthickness=0)
# reset_text = reset_canvas.create_text(100, 15, text="Press to reset: ", fill=WHITE, font=(FONT_NAME, 16, "normal"))
# reset_canvas.grid(column=0, row=5, pady=10)

reset_button = Button(text="Reset", bg=WHITE, command=reset, pady=5, font=(FONT_NAME, 14, "normal"), borderwidth=0)
reset_button.grid(column=1, row=5, pady=10)


window.mainloop()
