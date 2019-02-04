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

def clear():
    if not 'idlelib.run' in sys.modules:
        os.system("cls")

def wrap(text):
    text = text.center(shutil.get_terminal_size().columns, "=")
    return text

print(wrap("PREPERATION"))
root = tk.Tk()
root.withdraw()

print("Select File...")
file_path = filedialog.askopenfilename(filetypes = (("Word Documents","*.docx *.txt"),("All Files","*.*")))
print("{} Loaded... Processing".format(os.path.basename(file_path)))
if ".docx" in file_path:
    text = docx2txt.process(file_path)
else:
    with open(file_path) as f:
        text = f.readlines()
clear()
text = "".join(text)
origional = text

seed = str(hashlib.md5(text.encode()).hexdigest()) + str(os.urandom(20))
print("Generating seed using document")
print("seed =", seed)
random.seed(seed)
clear()
print(wrap("CORRUPTED {}".format(os.path.basename(file_path).upper())))
print("\n")
text = re.split('(\W)', text)
for i in range(len(text)):
    if text[i] != "\n":
        if random.choice([True, False, False]):
            length = len(text[i])
            replacement = ""
            for k in range(length):
                replacement += random.choice(["▄","█","▀","■","▓","▒","░"])
            text[i] = replacement
        
text = "".join(text)
print(text)
print(wrap(""))
input("Press any key to exit")
