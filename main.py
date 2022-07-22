from tkinter import *
import math

### 90% OF THE WORDS HAVE TO BE CORRECT IN ORDER TO EVALUATE TYPING SPEED ###

# Define duration of typing speed test
TESTING_TIME = 240
timer = None


# ------------ EVALUATE SCORE ------------ #
def compare(str1, str2, test_time):
    string1_words = set(str1.split())
    string2_words = set(str2.split())

    # Ignore following characters when comparing
    unwanted_characters = ".,!?"

    string1_words = {word.strip(unwanted_characters) for word in string1_words}
    string2_words = {word.strip(unwanted_characters) for word in string2_words}
    common_words = string1_words & string2_words

    # Message to the user who tried to type fast
    # 90% of words have to be correct in order to evaluate typing speed

    if len(common_words) > math.floor(len(string1_words)*0.9):
        if test_time < 20:
            title_label.config(text='You are Fast and Furious!', font=('Calibri', 20))
        else:
            title_label.config(text='You are sooooo slow!', font=('Calibri', 20))
    else:
        title_label.config(text='Please try again.\nTexts are not comparable!', font=('Calibri', 20))


# ------------ TIMER START ------------ #
def start_timer():
    retype_text_label.grid_forget()
    retype_text.grid(row=2, column=2, padx=15)

    # If test is started again delete previous typing
    retype_text.delete('1.0', END)


    title_label.config(text=f'How fast can you type?', font=('Calibri', 20))

    # Disable START button when pressed until STOP button is pressed. In order not to have multiple tests at once.
    start_btn.config(state='disabled')

    counter(1)


# ------------ TIMER RESET ------------ #
def reset_timer():
    window.after_cancel(timer)
    retype_text.grid_forget()
    retype_text_label.grid(row=2, column=2, padx=15)
    start_btn.config(state='normal')


    # Grab time that passed, from canvas item
    time_passed = canvas.itemcget(timer_text, 'text')
    t = time_passed.split(":")
    passed_min = int(t[0])
    passed_sec = int(t[1])
    test_time_sec = passed_min * 60 + passed_sec
    compare(sample_text.get("1.0", "end"), retype_text.get("1.0", "end"), test_time_sec)


    canvas.itemconfig(timer_text, text="0:00")


# ------------ COUNTER MECHANISM ------------ #

def counter(count):
    time_min = math.floor(count / 60)
    time_sec = count % 60

    if time_sec < 10:
        time_sec = f'0{time_sec}'

    canvas.itemconfig(timer_text, text=f'{time_min}:{time_sec}')

    if count < TESTING_TIME:
        global timer
        # After 1000 ms call "counter" function and pass count+1 as variable
        timer = window.after(1000, counter, count + 1)
    else:
        reset_timer()


window = Tk()
window.title('Typing Speed Test')
window.minsize(width=500, height=400)


title_label = Label(text=f'How fast can you type?', font=('Calibri', 20))
title_label.grid(row=0, column=1, pady=15)

canvas = Canvas(width=400, height=100)
timer_text = canvas.create_text(200, 50, text='0:00', font=('Calibri', 25, 'bold'))
canvas.grid(row=1, columnspan=3)


sample_text = Text(height=10, width=45)
sample_text.insert(END, "So close, no matter how far\nCouldn't be much more from the heart\nForever trusting who we are"
                        "\nAnd nothing else matters")
sample_text.grid(row=2, column=0, padx=15)

retype_text = Text(height=10, width=45)
retype_text.insert(END, "")

retype_text_label = Label(text='STEP1: Click START button to begin test.\n\nSTEP2: Retype text from left text column to'
                               ' the right one\n\nSTEP3: Click STOP button when you finish typing.',
                          font=('Calibri', 12), justify=LEFT)
retype_text_label.grid(row=2, column=2, padx=15)


start_btn = Button(text='START', width=15, command=start_timer)
start_btn.grid(row=3, column=1, sticky='w')

stop_btn = Button(text='STOP', width=15, command=reset_timer)
stop_btn.grid(row=3, column=1, sticky='e')

window.grid_rowconfigure(3, minsize=100)


# IN THE FUTURE: Store results in database and show first three places in window

window.mainloop()
