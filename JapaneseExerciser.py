import pandas as pd
import random
import PySimpleGUI as sg


class Kanji:
  def __init__(self, kanji, radicals, onyomi, romaji, meaning):
    self.kanji = kanji
    self.radicals = radicals
    self.onyomi = onyomi
    self.romaji = romaji
    self.meaning = meaning


# Read the dictionary excel
df = pd.read_excel('KanjiDictionary.xlsx')

# Create a global word list
word_list = []

# Read words
for index, row in df.iterrows():
    word = Kanji(row[0], row[1], row[2], row[3], row[4])
    word_list.append(word)

# Initialize for first run
word_count = len(word_list)
random_word = word_list[random.randint(0, word_count-1)]
question = "What " + random_word.kanji + " means?"
hint = "Hint: Radicals = " + random_word.radicals

# Layout settings
sg.theme('LightBrown13')
layout = [[sg.Text(question + "\n" + hint, key='-TEXT-', font=('Helvetica 11'))], [sg.InputText()], [sg.Button("Check"), sg.Button("Random")]]

# Create the window
window = sg.Window("JapaneseExerciser", layout)

# Create an event loop
while True:
    event, values = window.read()

    # Check input if "Check" button pressed
    if event == "Check":
        if values[0] == random_word.meaning.lower():
            sg.popup('Correct!')
        else:
            sg.popup("False! True answer was " + random_word.meaning)

    # Select random word for next run
    if event == "Random":
        random_word = word_list[random.randint(0, word_count-1)]
        question = "What " + random_word.kanji + " means?"
        hint = "Hint: Radicals = " + random_word.radicals
        window['-TEXT-'].update(question + "\n" + hint)

    # Close the program if window is closed
    if event == sg.WIN_CLOSED:
        break

window.close()



