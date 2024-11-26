import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do App")
        self.todo_file = "todos.json"
        self.todos = self.load_todos()

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.todo_input = tk.Entry(self.input_frame, width=40)
        self.todo_input.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self.input_frame, text="Add", command=self.add_todo)
        self.add_button.pack(side=tk.LEFT)

        self.todo_list = tk.Listbox(self.root, width=50, height=15, selectmode=tk.SINGLE)
        self.todo_list.pack(pady=10)
        self.todo_list.bind("<Double-Button-1>", self.edit_todo)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.complete_button = tk.Button(self.button_frame, text="Complete", command=self.complete_todo)
        self.complete_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_todo)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.show_completed_button = tk.Button(self.button_frame, text="Show Completed", command=self.show_completed)
        self.show_completed_button.pack(side=tk.LEFT, padx=5)

        self.show_active_button = tk.Button(self.button_frame, text="Show Active", command=self.show_active)
        self.show_active_button.pack(side=tk.LEFT, padx=5)

        self.load_todo_list()

    def load_todos(self):
        if os.path.exists(self.todo_file):
            with open(self.todo_file, 'r') as f:
                return json.load(f)
        return []

    def save_todos(self):
        with open(self.todo_file, 'w') as f:
            json.dump(self.todos, f, indent=4)

    def load_todo_list(self, filter_by=None):
        self.todo_list.delete(0, tk.END)
        for todo in self.todos:
            if filter_by == "completed" and not todo["completed"]:
                continue
            if filter_by == "active" and todo["completed"]:
                continue
            status = "[✓]" if todo["completed"] else "[ ]"
            self.todo_list.insert(tk.END, f"{status} {todo['text']} ({todo['date']})")

    def add_todo(self):
        text = self.todo_input.get().strip()
        if not text:
            messagebox.showwarning("Warning", "To-Do item cannot be empty!")
            return
        new_todo = {
            "text": text,
            "completed": False,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.todos.append(new_todo)
        self.save_todos()
        self.load_todo_list()
        self.todo_input.delete(0, tk.END)

    def complete_todo(self):
        selected = self.todo_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No to-do selected!")
            return
        index = selected[0]
        self.todos[index]["completed"] = True
        self.save_todos()
        self.load_todo_list()

    def delete_todo(self):
        selected = self.todo_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No to-do selected!")
            return
        index = selected[0]
        del self.todos[index]
        self.save_todos()
        self.load_todo_list()

    def edit_todo(self, event):
        selected = self.todo_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "No to-do selected!")
            return
        index = selected[0]
        current_text = self.todos[index]["text"]
        new_text = tk.simpledialog.askstring("Edit To-Do", "Edit your to-do:", initialvalue=current_text)
        if new_text:
            self.todos[index]["text"] = new_text
            self.save_todos()
            self.load_todo_list()

    def show_completed(self):
        self.load_todo_list(filter_by="completed")

    def show_active(self):
        self.load_todo_list(filter_by="active")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()