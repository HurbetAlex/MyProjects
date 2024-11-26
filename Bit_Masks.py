import tkinter as tk
from tkinter import ttk

cities = [
    ("Moscow", 3),
    ("Paris", 2),
    ("Berlin", 2),
    ("Brussels", 2),
    ("Amsterdam", 2),
    ("Rome", 2),
    ("London", 1),
    ("Dublin", 1),
    ("New York", -4),
    ("Washington, DC", -4),
    ("St. Louis", -5),
    ("Los Angeles", -7),
    ("Tokyo", 9),
    ("Beijing", 8),
    ("Ho Chi Minh City", 7),
    ("Mumbai", 5),
]

def create_bit_mask(offset):
    return 1 << (offset + 12)

def get_matching_cities(mask, negate=False):
    matching_cities = []
    for city, offset in cities:
        city_mask = create_bit_mask(offset)
        if (negate and not (mask & city_mask)) or (not negate and (mask & city_mask)):
            matching_cities.append(city)
    return matching_cities

def find_cities():
    try:
        gmt_offset = int(gmt_entry.get())
        if not -12 <= gmt_offset <= 12:
            output_label.config(text="Invalid GMT offset. Enter between -12 and 12.")
            return
        mask = create_bit_mask(gmt_offset)
        negate = negate_var.get()
        matching = get_matching_cities(mask, negate)
        count_label.config(text=f"Matching Cities: {len(matching)}")
        output_label.config(text="\n".join(matching) if matching else "No cities found.")
    except ValueError:
        output_label.config(text="Invalid input. Please enter an integer.")

app = tk.Tk()
app.title("Bit Mask City Finder")
app.geometry("400x500")

city_list_frame = ttk.Frame(app)
city_list_frame.pack(pady=10)
city_list_label = ttk.Label(city_list_frame, text="Cities and Timezones", font=("Helvetica", 14, "bold"))
city_list_label.pack()

city_list = "\n".join([f"{city}: GMT {offset:+d}" for city, offset in cities])
city_list_label = ttk.Label(city_list_frame, text=city_list, justify="left")
city_list_label.pack()

gmt_label = ttk.Label(app, text="Enter GMT Offset:")
gmt_label.pack(pady=5)
gmt_entry = ttk.Entry(app, width=10)
gmt_entry.pack(pady=5)

negate_var = tk.BooleanVar()
negate_checkbox = ttk.Checkbutton(app, text="Find cities NOT in GMT offset", variable=negate_var)
negate_checkbox.pack(pady=5)

find_button = ttk.Button(app, text="Find Cities", command=find_cities)
find_button.pack(pady=10)

count_label = ttk.Label(app, text="Matching Cities: 0", font=("Helvetica", 12))
count_label.pack(pady=5)

output_label = ttk.Label(app, text="", font=("Helvetica", 12), justify="left", wraplength=350)
output_label.pack(pady=10)

app.mainloop()
