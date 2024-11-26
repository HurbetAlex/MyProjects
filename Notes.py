import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import json
import datetime
import markdown

NOTES_FILE = "notes.json"

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes")
        self.notes = {}
        self.current_note = None
        self.load_notes()
        self.create_widgets()

    def create_widgets(self):
        self.sidebar = ttk.Frame(self.root, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.note_listbox = tk.Listbox(self.sidebar, height=20)
        self.note_listbox.pack(fill=tk.BOTH, expand=True)
        self.note_listbox.bind("<<ListBoxSelect>>", self.load_note)

        ttk.Button(self.sidebar, text="New Note", command=self.new_note).pack(fill=tk.X)
        ttk.Button(self.sidebar, text="Delete Note", command=self.delete_note).pack(fill=tk.X)

        self.editor_frame = ttk.Frame(self.root)
        self.editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.note_title = ttk.Entry(self.editor_frame, font=("arial", 16, "bold"))
        self.note_title.pack(fill=tk.X, pady=5)

        self.note_editor = ScrolledText(self.editor_frame, wrap=tk.WORD)
        self.note_editor.pack(fill=tk.BOTH, expand=True)

        self.save_button = ttk.Button(self.editor_frame, text="Save", command=self.save_note)
        self.save_button.pack(pady=5)

    def new_note(self):
        self.current_note = None
        self.note_title.delete(0, tk.END)
        self.note_editor.delete("1.0", tk.END)

    def delete_note(self):
        seleceted = self.note_listbox.curselection()
        if seleceted:
            note_title = self.note_listbox.get(seleceted)
            if messagebox.askyesno("Delete Note", f"Are you sure you want to delete '{note_title}'?"):
                del self.notes[note_title]
                self.save_to_file()
                self.update_note_listbox()
                self.new_note()

    def load_note(self, event=None):
        seleceted = self.note_listbox.curselection()
        if seleceted:
            note_title = self.note_listbox.get(seleceted)
            self.current_note = self.note_title
            note_data = self.notes[note_title]

            self.note_title.delete(0, tk.END)
            self.note_title.insert(0, note_title)

            self.note_editor.delete("1.0", tk.END)
            self.note_editor.insert("1.0", note_data["content"])

    def save_note(self):
        title = self.note_title.get().strip()
        content = self.note_editor.get("1.0", tk.END).strip()

        if not title:
            messagebox.showerror("Error", "Title is required")
            return

        self.notes[title] = {
            "content": content,
            "created": self.notes.get(title, {}).get("created", datetime.datetime.now().isoformat())
        }

        self.save_to_file()
        self.update_note_listbox()
        self.current_note = title

    def update_note_listbox(self):
        self.note_listbox.delete(0, tk.END)
        for note_title in sorted(self.notes.keys()):
            self.note_listbox.insert(tk.END, note_title)

    def save_to_file(self):
        with open(NOTES_FILE, "w") as f:
            json.dump(self.notes, f)

    def load_notes(self):
        try:
            with open(NOTES_FILE, "r") as f:
                self.notes = json.load(f)
        except FileNotFoundError:
            self.notes = {}

    def close_window(self):
        self.save_to_file()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_window)
    root.mainloop()