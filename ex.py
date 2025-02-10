from tkinter import *
from textblob import TextBlob
from gtts import gTTS
import os
from PyDictionary import PyDictionary
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysql@123",
    database="wise"
)

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS spellcheck (id INT AUTO_INCREMENT PRIMARY KEY, input_word VARCHAR(255), corrected_word VARCHAR(255), meaning TEXT)''')


root = Tk()
root.title("Spelling Checker")
root.geometry("600x600")
root.config(background="#dae6f6")

def check_spelling():
    word = enter_text.get()
    blob = TextBlob(word)
    corrected_text = str(blob.correct())

    # Save word, corrected word, and meaning into the database
    dictionary = PyDictionary()
    meaning = dictionary.meaning(corrected_text)
    meaning_text = "\n".join([f"{pos}: {', '.join(definitions)}" for pos, definitions in meaning.items()]) if meaning else "Meaning not found"
    cursor.execute("INSERT INTO spellcheck (input_word, corrected_word, meaning) VALUES (%s, %s, %s)", (word, corrected_text, meaning_text))
    conn.commit()

    cs = Label(root, text="Correct text:", font=("poppins", 20), bg="#dae6f6", fg="#364971")
    cs.grid(row=5, column=0, pady=9, columnspan=4)

    spell.config(text=corrected_text)

def auto_correct():
    word = enter_text.get()
    blob = TextBlob(word)
    auto_corrected_text = str(blob.correct())
    enter_text.delete(0, END)
    enter_text.insert(0, auto_corrected_text)

def get_meaning():
    word = enter_text.get()
    dictionary = PyDictionary()
    meaning = dictionary.meaning(word)
    if meaning:
        meaning_text = "\n".join([f"{pos}: {', '.join(definitions)}" for pos, definitions in meaning.items()])
        meaning_display.config(state=NORMAL)
        meaning_display.delete(1.0, END)
        meaning_display.insert(END, meaning_text)
        meaning_display.config(state=DISABLED)
    else:
        meaning_display.config(state=NORMAL)
        meaning_display.delete(1.0, END)
        meaning_display.insert(END, "Meaning not found")
        meaning_display.config(state=DISABLED)

heading = Label(root, text="Spelling Checker", font=("Trebuchet MS", 30, "bold"), bg="#dae6f6", fg="#364971")
heading.grid(row=0, column=0, pady=(50, 0), columnspan=2)

enter_text = Entry(root, justify="center", width=30, font=("poppins", 25), bg="white", border=2)
enter_text.grid(row=1, column=0, pady=10, columnspan=2)
enter_text.focus()

check_button = Button(root, text="Check", font=("arial", 20, "bold"), fg="white", bg="red", command=check_spelling)
check_button.grid(row=2, column=0, pady=5)

auto_correct_button = Button(root, text="Auto Correct", font=("arial", 20, "bold"), fg="white", bg="green", command=auto_correct)
auto_correct_button.grid(row=2, column=1, pady=5)

meaning_display = Text(root, font=("poppins", 15), bg="#dae6f6", fg="#364971", wrap=WORD, height=6, width=50)
meaning_display.grid(row=3, column=0, pady=10, columnspan=2)
meaning_display.config(state=DISABLED)

get_meaning_button = Button(root, text="Get Meaning", font=("arial", 20, "bold"), fg="white", bg="blue", command=get_meaning)
get_meaning_button.grid(row=4, column=0, pady=5, columnspan=2)

spell = Label(root, font=("poppins", 20), bg="#dae6f6", fg="#364971")
spell.grid(row=5, column=1, pady=10, columnspan=2)

root.mainloop()

