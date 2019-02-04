import random
import shutil
import docx2txt
import pprint
import re
import tkinter as tk
import sys
import os
import hashlib
import pip
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
    else:
        print("Reading generic file")
        with open(path) as f:
            text = f.readlines()
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


### PREPERATION ### 

print(wrap("PREPERATION"))
# load tkinter without creating a window in order to allow file dialogs
root = tk.Tk()
root.withdraw()


def main():
    """The main function, calls all other functions"""
    print("Select a File to corrupt")
    file_path = filedialog.askopenfilename(filetypes = (("Word Documents","*.docx *.txt"),("All Files","*.*")))
    text = read(file_path)
    generateSeed(text)
    print("{} Loaded...".format(os.path.basename(file_path)))
    clear()

    corrupted = corrupt(text)

    ### OUTPUT ###
    print(wrap("CORRUPTED {}".format(os.path.basename(file_path).upper())))
    print
    print("\n", corrupted)
    print(wrap(""))

main()
input("Press any key to exit")
    
    
    
