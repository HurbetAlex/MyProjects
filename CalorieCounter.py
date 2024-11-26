import tkinter as tk
from tkinter import ttk, messagebox
import json
import pandas as pd
from functools import partial

class CalorieCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Counter")
        self.data_file = "foods.json"
        self.load_data()
        self.results_per_page = 25
        self.current_page = 0
        self.filtered_results = []

        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(pady=10)

        self.input_label = tk.Label(self.search_frame, text="Food Description:")
        self.input_label.grid(row=0, column=0, padx=5)

        self.search_entry = tk.Entry(self.search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)

        self.search_button = tk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2, padx=5)

        self.clear_button = tk.Button(self.search_frame, text="Clear", command=self.clear_results)
        self.clear_button.grid(row=0, column=3, padx=5)

        self.result_count_label = tk.Label(self.root, text="Results: 0")
        self.result_count_label.pack()

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)

        self.result_tree = ttk.Treeview(self.result_frame, columns=("Food", "Portion", "Calories"), show="headings", height=15)
        self.result_tree.pack(side=tk.LEFT)

        self.result_tree.heading("Food", text="Food Description")
        self.result_tree.heading("Portion", text="Portion Size")
        self.result_tree.heading("Calories", text="Calories")

        self.scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.result_tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.result_tree.configure(yscroll=self.scrollbar.set)

        self.pagination_frame = tk.Frame(self.root)
        self.pagination_frame.pack(pady=10)

        self.more_button = tk.Button(self.pagination_frame, text="Show More", command=self.load_more_results)
        self.more_button.pack()

    def load_data(self):
        if not self.data_file:
            data = pd.read_excel("MyPyramidData.xlsx")
            data = data[["Food Description", "Portion Size", "Calories"]]
            data.to_json(self.data_file, orient="records")
        with open(self.data_file, "r") as f:
            self.data = json.load(f)

    def search(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Warning", "Please enter a search term.")
            return
        self.filtered_results = [
            food for food in self.data
            if query in food["Food Description"].lower()
        ]
        if not self.filtered_results:
            messagebox.showinfo("Info", "No matching food items found.")
        self.current_page = 0
        self.display_results()

    def display_results(self):
        self.result_tree.delete(*self.result_tree.get_children())
        start = self.current_page * self.results_per_page
        end = start + self.results_per_page
        for item in self.filtered_results[start:end]:
            self.result_tree.insert("", tk.END, values=(item["Food Description"], item["Portion Size"], item["Calories"]))
        self.result_count_label.config(text=f"Results: {len(self.filtered_results)}")

    def clear_results(self):
        self.search_entry.delete(0, tk.END)
        self.result_tree.delete(*self.result_tree.get_children())
        self.result_count_label.config(text="Results: 0")
        self.filtered_results = []
        self.current_page = 0

    def load_more_results(self):
        if self.current_page * self.results_per_page >= len(self.filtered_results):
            return
        self.current_page += 1
        self.display_results()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieCounterApp(root)
    root.mainloop()
