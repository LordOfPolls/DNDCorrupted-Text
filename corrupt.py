import random
import shutil
import docx2txt
import pprint
import re
import tkinter as tk
import sys
import os
import hashlib
import PyPDF2
from tkinter import filedialog


### UTILITY FUNCTIONS ###
def clear():
    """Checks if the script is running in idle, if it isnt, it clears the screen"""
    if not 'idlelib.run' in sys.modules:
        os.system("cls")


def wrap(text):
    """Surrounds the text with = to make titles"""
    text = text.center(shutil.get_terminal_size().columns, "=")
    return text


def read(path):
    """Reads the selected file into a string"""
    if ".docx" in path:
        print("Reading docx file")
        text = docx2txt.process(path)
    elif ".txt" in path:
        print("Reading txt file")
        with open(path) as f:
            text = f.readlines()
        pprint.pprint(text)
    elif ".pdf" in path:
        print("Reading PDF...")
        file = open(path, 'rb')
        PDF = PyPDF2.PdfFileReader(file)

        # This script will only ever read 2 pages because reading pdf pages takes AGES
        if PDF.numPages > 2:
            print("Note: This code will only read two pages due to the fact PDFs take a long time to process")
            input("Press return to continue")
        text = PDF.getPage(0).extractText()
        if PDF.numPages > 1:
            text += "\n\n"
            text += PDF.getPage(1).extractText()
    else:
        print("Unsupported filetype. This code only supports:\n\n.txt\n.pdf\n.docx")
        main()
        return
        
    text = "".join(text)
    return text


def generateSeed(text):
    """Generates a seed using the MD5 of the text, not necessary"""
    seed = str(hashlib.md5(text.encode()).hexdigest())
    random.seed(seed)


def corrupt(text):
    """The code that actually corrupts the text"""
    text = re.split('(\W)', text)
    for i in range(len(text)):
        if text[i] != "\n":
            if random.choice([True, False, False]):
                length = len(text[i])
                replacement = ""
                for k in range(length):
                    replacement += random.choice(["▄","█","▀","■","▓","▒","░"])
                text[i] = replacement
    
    return "".join(text)


### PREPARATION ###

print(wrap("PREPARATION"))
# load tkinter without creating a window in order to allow file dialogs
root = tk.Tk()
root.withdraw()


def main():
    """The main function, calls all other functions"""
    print("Select a File to corrupt")
    file_path = filedialog.askopenfilename(title="Select file to corrupt",
                                           filetypes=(("Supported","*.docx *.txt *.pdf"),("All Files","*.*")))
    if not file_path:
        exit()
    text = read(file_path)
    generateSeed(text)
    print("{} Loaded...".format(os.path.basename(file_path)))
    clear()

    corrupted = corrupt(text)

    ### OUTPUT ###
    print(wrap("CORRUPTED {}".format(os.path.basename(file_path).upper())))
    print("\n", corrupted)
    print(wrap(""))


main()
input("Press return to exit")
