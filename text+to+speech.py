#     from tkinter import filedialog

#     from tkinter.filedialog import askopenfilename

#     from tkinter.scrolledtext import ScrolledText

#     from tkinter import *

#     import speech_recognition as sr
#     import pyaudio



# import tkinter as tk

# import os

# import re

# import sys

# ################ FUNCTIONS ################


# def print_to_textbox(wordlist):
#     """Print all lines in wordlist to textbox"""
#     for lines in wordlist:
#         text_box.insert("end", "\n"+lines)
#     if len(wordlist) == 0:
#         text_box.insert("1.0", "\nNothing To Display")

# def browse_button():
#     """Button will open a window for directory selection"""
#     global foh
#     selected_directory = askopenfilename()
#     foh=selected_directory
#     print(selected_directory)



# def totext():
#     textp=""
#     r = sr.Recognizer()

#     audio= foh #uncomment to insert a audio file

#     #with sr.Microphone() as source:
#     with sr.AudioFile(audio) as source:   #comment the above method and uncomment this line to enable read AudioFile
#         print('Audio analysed')
#         #   audio = r.record(source)    comment the next two line and uncomment
#         #r.adjust_for_ambient_noise(source, duration=5)
#         audio = r.listen(source)
#         try:
#             print('Dellavi thinks you said \n' + r.recognize_google(audio))
#             text =r.recognize_google(audio)                                   # comment the above line and uncomment the followinf lines
#             print(text)
#             textp=textp+text

#         except Exception as e:
#             print(e)

#     text_box.insert(INSERT, textp)
    


# # Setup Window.
# window = tk.Tk()
# window.geometry("900x500")
# window.title("String Search")

# # Button to select directory.
# select_directory = tk.Button(window, text = "Select Wav File", command=browse_button)
# select_directory.pack()



# # Button to run main script.
# go_button = tk.Button(window, text="Go", command=totext)
# go_button.pack()



# # Text box to display output of main text.
# text_box = ScrolledText(width=110, borderwidth=2, relief="sunken", padx=20)
# text_box.pack()

# # Button to clear the text box display.
# clear_button = tk.Button(window, text = "Clear", command = lambda: text_box.delete("1.0", tk.END))
# clear_button.pack()

# # Run an event loop.
# window.mainloop()
from datetime import datetime as dt
now=dt.now()
ct = now.strftime("%H:%M:%S") 
print(ct)