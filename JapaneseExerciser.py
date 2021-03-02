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
layout = [[sg.Text(question + "\n" + hint, key='-TEXT-', font=('Noto Sans JP Medium', 11), size=(25, 2))],
          [sg.InputText(), sg.Button("Check")], [sg.Button("Details"), sg.Button("Notes"), sg.Button("Next Random")]]

# Create the window
window = sg.Window("JapaneseExerciser", layout)

# Store wrong answers
wrong_ans = []

# Create an event loop
while True:
    event, values = window.read()

    # Check input if "Check" button pressed
    if event == "Check":
        if values[0] == random_word.meaning.lower():
            sg.popup('Correct!')
            if random_word in wrong_ans:  # if user corrects her/his mistake remove from notes list
                wrong_ans.remove(random_word)

        elif values[0] == "":
            sg.popup("You did not enter anything!")

        else:
            sg.popup("False! True answer was " + random_word.meaning)
            if random_word not in wrong_ans:  # if user makes a mistake, note that word
                wrong_ans.append(random_word)

    # Select random word for next run
    if event == "Next Random":
        random_word = word_list[random.randint(0, word_count-1)]
        question = "What " + random_word.kanji + " means?"
        hint = "Hint: Radicals = " + random_word.radicals
        window['-TEXT-'].update(question + "\n" + hint)

    # Print details about word
    if event == "Details":
        sg.popup("Onyomi-Kunyomi: " + random_word.onyomi + "\nRomaji: " + random_word.romaji, font=('Noto Sans JP Medium', 10))

    if event == "Notes":
        message = "Please remember these:"
        for word in wrong_ans:
            message += "\nKanji: " + word.kanji + "\tMeaning: " + word.meaning
        sg.popup(message)

    # Close the program if window is closed
    if event == sg.WIN_CLOSED:
        break

window.close()



