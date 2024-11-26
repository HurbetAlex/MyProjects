import tkinter as tk
from tkinter import simpledialog, scrolledtext, filedialog, messagebox
from tkinter.font import Font
import os

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")
        self.username = simpledialog.askstring("Username", "Enter your username:")
        if not self.username:
            self.username = "Anonymous"

        self.chat_frame = tk.Frame(self.root)
        self.chat_frame.pack(pady=10, padx=10)

        self.chat_box = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, width=60, height=20, state=tk.DISABLED)
        self.chat_box.pack(pady=5)

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)

        self.message_entry = tk.Entry(self.input_frame, width=50)
        self.message_entry.grid(row=0, column=0, padx=5)
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=5)

        self.emoji_button = tk.Button(self.input_frame, text="😊", command=self.add_emoji)
        self.emoji_button.grid(row=0, column=2, padx=5)

        self.file_button = tk.Button(self.input_frame, text="📎", command=self.send_file)
        self.file_button.grid(row=0, column=3, padx=5)

    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        self.display_message(f"{self.username}: {message}")
        self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, message + "\n")
        self.chat_box.see(tk.END)
        self.chat_box.config(state=tk.DISABLED)

    def add_emoji(self):
        emojis = ["😊", "😂", "❤️", "👍", "😢", "😡", "🎉"]
        selected_emoji = simpledialog.askstring("Choose Emoji", "Enter emoji:\n" + " ".join(emojis))
        if selected_emoji in emojis:
            self.message_entry.insert(tk.END, selected_emoji)

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            self.display_message(f"{self.username} sent a file: {file_name}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
