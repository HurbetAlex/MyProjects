import tkinter as tk
from tkinter import ttk
import requests

def fetch_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def convert_currency():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get()
        to_currency = to_currency_var.get()
        if from_currency == to_currency:
            converted_amount = amount
        else:
            rate = rates[to_currency] / rates[from_currency]
            converted_amount = round(amount * rate, 2)
        result_label.config(text=f"Converted Amount: {converted_amount} {to_currency}")
    except ValueError:
        result_label.config(text="Error: Please enter a valid number")

def swap_currencies():
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    from_currency_var.set(to_currency)
    to_currency_var.set(from_currency)
    convert_currency()

app = tk.Tk()
app.title("Currency Converter")
app.geometry("400x300")

exchange_data = fetch_exchange_rates()
if exchange_data:
    rates = exchange_data["rates"]
    currencies = sorted(rates.keys())

    amount_label = ttk.Label(app, text="Amount:")
    amount_label.pack(pady=5)

    amount_entry = ttk.Entry(app, width=20)
    amount_entry.pack(pady=5)

    from_currency_label = ttk.Label(app, text="From Currency:")
    from_currency_label.pack(pady=5)

    from_currency_var = tk.StringVar()
    from_currency_dropdown = ttk.Combobox(app, textvariable=from_currency_var, values=currencies, state="readonly")
    from_currency_dropdown.pack(pady=5)
    from_currency_dropdown.set("USD")

    to_currency_label = ttk.Label(app, text="To Currency:")
    to_currency_label.pack(pady=5)

    to_currency_var = tk.StringVar()
    to_currency_dropdown = ttk.Combobox(app, textvariable=to_currency_var, values=currencies, state="readonly")
    to_currency_dropdown.pack(pady=5)
    to_currency_dropdown.set("EUR")

    convert_button = ttk.Button(app, text="Convert", command=convert_currency)
    convert_button.pack(pady=10)

    swap_button = ttk.Button(app, text="Swap Currencies", command=swap_currencies)
    swap_button.pack(pady=5)

    result_label = ttk.Label(app, text="Converted Amount: ")
    result_label.pack(pady=10)

    amount_entry.bind("<KeyRelease>", lambda e: convert_currency())
    from_currency_dropdown.bind("<<ComboboxSelected>>", lambda e: convert_currency())
    to_currency_dropdown.bind("<<ComboboxSelected>>", lambda e: convert_currency())

app.mainloop()
