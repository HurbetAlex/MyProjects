import os
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time
import json
import sqlite3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SlackArchiver:
    def __init__(self, root):
        self.root = root
        self.root.title("Slack Archiver")
        self.slack_token = os.getenv("SLACK_API_TOKEN")
        self.client = WebClient(token=self.slack_token)
        self.archiving = False

        self.channels = []
        self.db_name = "slack_archive.db"
        self.setup_db()

        self.build_ui()

    def setup_db(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                channel TEXT,
                user TEXT,
                text TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

    def build_ui(self):
        self.channel_frame = tk.Frame(self.root)
        self.channel_frame.pack(pady=10)

        self.channel_label = tk.Label(self.channel_frame, text="Channels to Archive:")
        self.channel_label.pack()

        self.channel_listbox = tk.Listbox(self.channel_frame, width=40, height=10)
        self.channel_listbox.pack()

        self.add_channel_button = tk.Button(self.channel_frame, text="Add Channel", command=self.add_channel)
        self.add_channel_button.pack(side=tk.LEFT, padx=5)

        self.remove_channel_button = tk.Button(self.channel_frame, text="Remove Channel", command=self.remove_channel)
        self.remove_channel_button.pack(side=tk.LEFT, padx=5)

        self.archive_frame = tk.Frame(self.root)
        self.archive_frame.pack(pady=10)

        self.start_archive_button = tk.Button(self.archive_frame, text="Start Archiving", command=self.start_archiving)
        self.start_archive_button.pack(side=tk.LEFT, padx=5)

        self.stop_archive_button = tk.Button(self.archive_frame, text="Stop Archiving", command=self.stop_archiving)
        self.stop_archive_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(self.archive_frame, text="Export to File", command=self.export_to_file)
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.root, text="Status: Idle", fg="green")
        self.status_label.pack(pady=10)

    def add_channel(self):
        channel_name = tk.simpledialog.askstring("Add Channel", "Enter channel name:")
        if channel_name:
            try:
                response = self.client.conversations_list()
                for channel in response["channels"]:
                    if channel["name"] == channel_name:
                        self.channels.append(channel["id"])
                        self.channel_listbox.insert(tk.END, channel_name)
                        return
                messagebox.showerror("Error", "Channel not found.")
            except SlackApiError as e:
                messagebox.showerror("Error", f"Slack API error: {e.response['error']}")

    def remove_channel(self):
        selected = self.channel_listbox.curselection()
        if selected:
            index = selected[0]
            self.channel_listbox.delete(index)
            del self.channels[index]

    def start_archiving(self):
        if self.archiving:
            messagebox.showwarning("Warning", "Archiving already in progress.")
            return
        if not self.channels:
            messagebox.showwarning("Warning", "No channels to archive.")
            return
        self.archiving = True
        self.status_label.config(text="Status: Archiving", fg="blue")
        threading.Thread(target=self.archive_channels, daemon=True).start()

    def stop_archiving(self):
        self.archiving = False
        self.status_label.config(text="Status: Idle", fg="green")

    def archive_channels(self):
        while self.archiving:
            for channel in self.channels:
                try:
                    last_ts = self.get_last_timestamp(channel)
                    response = self.client.conversations_history(channel=channel, oldest=last_ts)
                    for message in response["messages"]:
                        self.save_message(channel, message)
                except SlackApiError as e:
                    messagebox.showerror("Error", f"Slack API error: {e.response['error']}")
            time.sleep(60)

    def get_last_timestamp(self, channel):
        self.cursor.execute("SELECT MAX(timestamp) FROM messages WHERE channel = ?", (channel,))
        result = self.cursor.fetchone()
        return result[0] if result and result[0] else "0"

    def save_message(self, channel, message):
        try:
            self.cursor.execute("""
                INSERT INTO messages (id, channel, user, text, timestamp) VALUES (?, ?, ?, ?, ?)
            """, (message["client_msg_id"], channel, message.get("user", "unknown"), message.get("text", ""), message["ts"]))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def export_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            self.cursor.execute("SELECT * FROM messages")
            messages = [{"id": row[0], "channel": row[1], "user": row[2], "text": row[3], "timestamp": row[4]} for row in self.cursor.fetchall()]
            with open(file_path, "w") as file:
                json.dump(messages, file, indent=4)
            messagebox.showinfo("Export Complete", f"Messages exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SlackArchiver(root)
    root.mainloop()
