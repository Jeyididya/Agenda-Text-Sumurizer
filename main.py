import tkinter
from tkinter import *
from tkinter import messagebox
import sounddevice as sound
from scipy.io.wavfile import write
import wavio as wv
import time
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import speech_recognition as sr
import pyaudio
from datetime import datetime as dt

#file checking library
import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

def read_article(file_name):
    file = open(file_name, 'r')
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


def sentence_similarity(sent1,sent2,stopwords=None):
        if stopwords is None:
            stopwords=[]
        sent1 = [w.lower() for w in sent1]
        sent2 = [w.lower() for w in sent2]
        all_words = list(set(sent1+sent2))
        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)
        for w in sent1:
            if w in stopwords:
                continue
            vector1[all_words.index(w)] +=1
        for w in sent2:
            if w in stopwords:
                continue
            vector2[all_words.index(w)] +=1
        return 1-cosine_distance(vector1,vector2)

def gen_sim_matrix(sentences, stop_words):
        similarity_matrix=np.zeros((len(sentences),len(sentences)))
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 ==idx2:
                    continue
                similarity_matrix[idx1][idx2]=sentence_similarity(sentences[idx1],sentences[idx2],stop_words)
        return similarity_matrix

def generate_summary(file_name, top_n=5):
    
    stop_words=stopwords.words('english')
    summarize_text=[]
    sentences = read_article(file_name)
    sentence_similarity_matrix=gen_sim_matrix(sentences,stop_words)
    sentence_similarity_graph=nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence=sorted(((scores[i],s)for i,s in enumerate(sentences)), reverse=True)
    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))
    te=". ".join(summarize_text)
    print("summary \n",te)
    return te

#generate_summary("asd.txt", 1)

"""def all(file_name,top_n=5):
    read_article(file_name)
    sentence_similarity(sent1,sent2,stopwords=None)
    gen_sim_matrix(sentences, stop_words)
    generate_summary(file_name, top_n)

"""

#########################

#setting up the audio configuration
import tkinter as tk
import os
import re
import sys


window = tkinter.Tk()
window.geometry("520x300")
window.title("Agenda Meeting Summarizer")
window.resizable(False,False)
window.configure(bg="#072227")

duration = ""#StringVar(record_window)
text_box=""
text_box2=""


#functions to speech to text
def sumsum():
    text=generate_summary(fohm,1)
    for lines in text:
        text_box2.insert("end",lines)




def print_to_textbox(wordlist):
    """Print all lines in wordlist to textbox"""
    for lines in wordlist:
        text_box.insert("end", "\n"+lines)
    if len(wordlist) == 0:
        text_box.insert("1.0", "\nNothing To Display")

def browse_button():
    """Button will open a window for directory selection"""
    global foh
    selected_directory = askopenfilename()
    foh=selected_directory
    print(selected_directory)

def browse_button_sum():
    """Button will open a window for directory selection"""
    global fohm
    selected_directory = askopenfilename()
    fohm=selected_directory
    print("m",selected_directory)


def totext():
    global text_box
    textp=""
    r = sr.Recognizer()

    audio= foh #uncomment to insert a audio file

    #with sr.Microphone() as source:
    with sr.AudioFile(audio) as source:   #comment the above method and uncomment this line to enable read AudioFile
        print('Audio analysed')
        #   audio = r.record(source)    comment the next two line and uncomment
        #r.adjust_for_ambient_noise(source, duration=5)
        audio = r.listen(source)
        te=""
        fi=open('toSpeech.txt','w')
        try:
            text =r.recognize_google(audio)                                   # comment the above line and uncomment the followinf lines
            print(text)
            textp=textp+text
            for i in text:
                fi.write(i)

        except Exception as e:
            print(e)

    text_box.insert(INSERT, textp)
    


#Recording audio function to embed in record audio gui
def record_audio():
    freq = 44100
    dur = int(duration.get())
    recording = sound.rec(dur*freq, samplerate=freq, channels=2)
    try:
        temp=int(duration.get())
    except:
        print("please enter the correct value ")
    while temp>0:
        record_window.update()
        time.sleep(1)
        temp-=1
        if(temp==0):
            messagebox.showinfo("Time Countdown", "Time's up")
        Label(record_window, text=f"{str(temp)}", width=4).place(x=240, y=590)
    sound.wait()
    now=dt.now()
    ct = now.strftime("%H:%M:%S")
    record="record" + ct
    write(record+".wav", freq, recording)


#Record audio GUI
def record():
    global duration,record_window
    record_window = tkinter.Tk()
    duration=StringVar(record_window)
    
    record_window.geometry("300x400")
    record_window.resizable(False, False)
    record_window.title("Record Meeting")
    #voice recorder label
    record_text = tkinter.Label(record_window, text="Voice Recorder", font="arial 20 bold").pack(pady=15)
    entry = tkinter.Entry(record_window, textvariable=duration, font="arial 10", width=15 ).pack(pady=10)
    Label(record_window,text="Enter time in seconds", font="arial").pack(pady=10)
    record_button = tkinter.Button(record_window, text="Record", command=record_audio).pack(pady=10)

#Summarize text GUI
def summarize():
    global text_box2
    summarize_window = tkinter.Tk()
    summarize_window.geometry("900x300")
    summarize_window.title("Summarize Meeting")
    select_directory = tk.Button(summarize_window, text = "Select Text File", command=browse_button_sum)
    select_directory.pack()



    # Button clearto run main script.
    go_button = tk.Button(summarize_window, text="Go", command=sumsum)
    go_button.pack()



    # Text box to display output of main text.
    text_box2 = ScrolledText(summarize_window,width=110, borderwidth=2, relief="sunken", padx=20)
    text_box2.pack()

    # Button to clear the text box display.
    clear_button = tk.Button(summarize_window, text = "Clear", command = lambda: text_box.delete("1.0", tk.END))
    clear_button.pack()
    

#speech to text converter GUI
def speechToText():
    global text_box
    swindow = tk.Tk()
    swindow.geometry("900x500")
    swindow.title("String Search")

    # Button to select directory.
    select_directory = tk.Button(swindow, text = "Select Wav File", command=browse_button)
    select_directory.pack()



    # Button clearto run main script.
    go_button = tk.Button(swindow, text="Go", command=totext)
    go_button.pack()



    # Text box to display output of main text.
    text_box = ScrolledText(swindow,width=110, borderwidth=2, relief="sunken", padx=20)
    text_box.pack()

    # Button to clear the text box display.
    clear_button = tk.Button(swindow, text = "Clear", command = lambda: text_box.delete("1.0", tk.END))
    clear_button.pack()


frame = tkinter.Frame(window).pack()
record = tkinter.Button(frame, text="Record", fg="white",bg="#35858B", command=record, height=10, width=15).pack(side = "left",padx="10")
SpeechToText = tkinter.Button(frame, text="Speech To Text", fg="white",bg="#35858B", command=speechToText, height=10, width=15).pack(side = "left",padx="10")
summarize = tkinter.Button(frame, text="Summarize", fg="white", bg="#35858B", command=summarize, height=10, width=15).pack(side = "left",padx="10")

#Main runner 
window.mainloop()
