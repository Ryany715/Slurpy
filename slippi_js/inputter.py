from tkinter import *
from tkinter import filedialog
from flask import Flask, render_template, request
import os
import requests

def callback():
    # function using allows the user to pick a file of filetype
    filename = filedialog.askopenfilename(initialdir = '/', title = 'Select a File',filetypes = (('Slippi files','*.slp*'),('all files','*.*')))
    label_file_explorer.configure(text='File Opened: '+ filename)
    # this will send the slp file to Flask
    url = 'http://127.0.0.1:54321'
    files = {'file': (filename, open(filename, 'rb'), 'application/pdf', {'Expires': '0'})}
    reply = requests.post(url = url, files = files)


root = Tk() 
root.title('Melee Stat Tracker')
root.geometry('900x600')
bg = PhotoImage(file = os.path.dirname(__file__) + '\\fixtures\SSBU-Pokémon_Stadium.png')
label1 = Label(root, image = bg, anchor=CENTER)
label1.place(x = 0, y = 0)
label_file_explorer = Label(root, width = 65, height = 2, fg = 'white', bg = 'gray')
button_browse = Button(root, text = 'Browse', command = callback)
button_exit = Button(root, text = 'Exit', command = exit)

# place the buttons where they need to go
label_file_explorer.place(x = 315, y= 300, anchor = CENTER)
button_browse.place(x = 600, y = 290, anchor = CENTER)
button_exit.place(x = 600, y = 315, anchor = CENTER)

# keep the window open
root.mainloop()
#newlabel = root.Label(test = "Upload Slippi .SLP: ")
