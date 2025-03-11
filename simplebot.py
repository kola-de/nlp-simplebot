# WRITE YOUR CODE HERE

from openai import OpenAI
from tkinter import *
import tkinter.scrolledtext as tks
from datetime import datetime
import os

# CODIO SOLUTION BEGIN
# Initialize the OpenAI client with the API key
client = OpenAI()

# Generating response using updated gpt-4o-mini-turbo model with chat completions
def get_bot_response(user_input):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant chatbot."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# Function to create and insert user message into the chat window
def create_and_insert_user_frame(user_input):
    userFrame = Frame(chatWindow, bg="#d0ffff")
    Label(userFrame, text=user_input, font=("Arial", 11), bg="#d0ffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    Label(userFrame, text=datetime.now().strftime("%H:%M"), font=("Arial", 7), bg="#d0ffff").grid(row=1, column=0, sticky="w")
    chatWindow.insert('end', '\n ', 'tag-right')
    chatWindow.window_create('end', window=userFrame)

# Function to create and insert bot response into the chat window
def create_and_insert_bot_frame(bot_response):
    botFrame = Frame(chatWindow, bg="#ffffd0")
    Label(botFrame, text=bot_response, font=("Arial", 11), bg="#ffffd0", wraplength=400, justify='left').grid(row=0, column=0, sticky="w", padx=5, pady=5)
    Label(botFrame, text=datetime.now().strftime("%H:%M"), font=("Arial", 7), bg="#ffffd0").grid(row=1, column=0, sticky="w")
    chatWindow.insert('end', '\n ', 'tag-left')
    chatWindow.window_create('end', window=botFrame)
    chatWindow.insert(END, "\n\n" + "")

# Function to send messages
def send(event=None):
    chatWindow.config(state=NORMAL)
    user_input = userEntryBox.get("1.0","end").strip()
    if user_input:
        bot_response = get_bot_response(user_input)
        create_and_insert_user_frame(user_input)
        create_and_insert_bot_frame(bot_response)
        chatWindow.config(state=DISABLED)
        userEntryBox.delete("1.0","end")
        chatWindow.see('end')

# Main window setup
baseWindow = Tk()
baseWindow.title("The Simple Bot")
baseWindow.geometry("500x250")

chatWindow = tks.ScrolledText(baseWindow, font="Arial")
chatWindow.tag_configure('tag-left', justify='left')
chatWindow.tag_configure('tag-right', justify='right')
chatWindow.config(state=DISABLED)

sendButton = Button(baseWindow, font=("Verdana", 12, 'bold'), text="Send", bg="#fd94b4", activebackground="#ff467e", fg='#ffffff', command=send)
sendButton.bind("<Button-1>", send)
baseWindow.bind('<Return>', send)

userEntryBox = Text(baseWindow, bd=1, bg="white", width=38, font="Arial")
chatWindow.place(x=1, y=1, height=200, width=500)
userEntryBox.place(x=3, y=202, height=27)
sendButton.place(x=430, y=200)

baseWindow.mainloop()
# CODIO SOLUTION END      