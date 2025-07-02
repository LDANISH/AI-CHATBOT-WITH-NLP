import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Load FAQ data
faq_df = pd.read_csv("faq.csv")

# Get best response function
def get_best_response(user_input):
    user_doc = nlp(user_input.lower())
    best_score = 0
    best_response = "🤖 Sorry, I don't understand. Can you rephrase?"

    for _, row in faq_df.iterrows():
        question_doc = nlp(str(row['question']).lower())
        score = user_doc.similarity(question_doc)
        if score > best_score and score > 0.75:
            best_score = score
            best_response = row['answer']

    return best_response

# Handle user input
def handle_input():
    user_input = entry.get()
    if user_input.strip() == "":
        return
    chat_window.config(state='normal')
    chat_window.insert(tk.END, f"You: {user_input}\n", 'user')
    bot_response = get_best_response(user_input)
    chat_window.insert(tk.END, f"Bot: {bot_response}\n\n", 'bot')
    chat_window.config(state='disabled')
    entry.delete(0, tk.END)

# Setup GUI window
root = tk.Tk()
root.title("SmartBot - MINIbot")

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=("Arial", 12))
chat_window.pack(padx=10, pady=10)
chat_window.tag_config('user', foreground='blue')
chat_window.tag_config('bot', foreground='green')
chat_window.config(state='disabled')

entry = tk.Entry(root, font=("Arial", 12), width=45)
entry.pack(side=tk.LEFT, padx=(10, 0), pady=(0, 10))

send_button = tk.Button(root, text="Send", command=handle_input, font=("Arial", 12))
send_button.pack(side=tk.LEFT, padx=(5, 10), pady=(0, 10))

# Run the GUI loop
root.mainloop()
