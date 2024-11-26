import tkinter as tk
from tkinter import ttk
import random
import string
import pyperclip

def generate_password():
    length = length_var.get()
    include_uppercase = uppercase_var.get()
    include_lowercase = lowercase_var.get()
    include_numbers = numbers_var.get()
    include_symbols = symbols_var.get()

    if not (include_uppercase or include_lowercase or include_numbers or include_symbols):
        password_var.set("Select at least one option!")
        return

    character_pool = ""
    if include_uppercase:
        character_pool += string.ascii_uppercase
    if include_lowercase:
        character_pool += string.ascii_lowercase
    if include_numbers:
        character_pool += string.digits
    if include_symbols:
        character_pool += string.punctuation

    password = "".join(random.choice(character_pool) for _ in range(length))
    password_var.set(password)
    update_strength(password)

def copy_to_clipboard():
    pyperclip.copy(password_var.get())

def update_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length >= 12 and score >= 3:
        strength_label.config(text="Strength: Strong", foreground="green")
    elif length >= 8 and score >= 2:
        strength_label.config(text="Strength: Medium", foreground="orange")
    else:
        strength_label.config(text="Strength: Weak", foreground="red")

app = tk.Tk()
app.title("Password Generator")
app.geometry("400x400")

frame = ttk.Frame(app, padding="10")
frame.pack(expand=True, fill="both")

length_var = tk.IntVar(value=8)
uppercase_var = tk.BooleanVar(value=True)
lowercase_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)
password_var = tk.StringVar(value="")

ttk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="w", pady=5)
length_slider = ttk.Scale(frame, from_=4, to=30, variable=length_var, orient="horizontal")
length_slider.grid(row=0, column=1, pady=5, sticky="ew")

ttk.Checkbutton(frame, text="Include Uppercase Letters", variable=uppercase_var).grid(row=1, column=0, columnspan=2, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Include Lowercase Letters", variable=lowercase_var).grid(row=2, column=0, columnspan=2, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Include Numbers", variable=numbers_var).grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Include Symbols", variable=symbols_var).grid(row=4, column=0, columnspan=2, sticky="w", pady=5)

generate_button = ttk.Button(frame, text="Generate Password", command=generate_password)
generate_button.grid(row=5, column=0, columnspan=2, pady=10)

ttk.Entry(frame, textvariable=password_var, state="readonly", font=("Helvetica", 12)).grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")
copy_button = ttk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=7, column=0, columnspan=2, pady=5)

strength_label = ttk.Label(frame, text="Strength: ", font=("Helvetica", 10))
strength_label.grid(row=8, column=0, columnspan=2, pady=5)

app.mainloop()
