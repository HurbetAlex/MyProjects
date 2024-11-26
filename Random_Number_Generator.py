import tkinter as tk
from tkinter import ttk
import random

def generate_random_number():
    try:
        min_value = float(min_entry.get()) if decimal_var.get() else int(min_entry.get())
        max_value = float(max_entry.get()) if decimal_var.get() else int(max_entry.get())

        if min_value > max_value:
            result_label.config(text="Error: Min value must be <= Max value")
            return

        if decimal_var.get():
            random_number = round(random.uniform(min_value, max_value), 2)
        else:
            random_number = random.randint(int(min_value), int(max_value))

        result_label.config(text=f"Random number: {random_number}")

    except:
        result_label.config(text="Error: Invalid input")

app = tk.Tk()
app.title("Random Number Generator")
app.geometry("400x300")

title_label = ttk.Label(app, text="Random Number Generator", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

min_frame = ttk.Frame(app)
min_frame.pack(pady=5)
min_label = ttk.Label(min_frame, text="Min Value:")
min_label.pack(side="left", padx=5)
min_entry = ttk.Entry(min_frame, width=10)
min_entry.pack(side="left")

max_frame = ttk.Frame(app)
max_frame.pack(pady=5)
max_label = ttk.Label(max_frame, text="Max Value:")
max_label.pack(side="left", padx=5)
max_entry = ttk.Entry(max_frame, width=10)
max_entry.pack(side="left")

decimal_var = tk.BooleanVar(value=False)
decimal_checkbox = ttk.Checkbutton(app, text="Allow Decimals", variable=decimal_var)
decimal_checkbox.pack(pady=5)

generate_button = ttk.Button(app, text="Generate", command=generate_random_number)
generate_button.pack(pady=10)

result_label = ttk.Label(app, text="Random Number: ", font=("Helvetica", 12))
result_label.pack(pady=10)

app.mainloop()