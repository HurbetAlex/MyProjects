import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import threading
import time
import json

#Это файл для хранения событий
EVENTS_FILE = 'events.json'

# Создаю глобальную переменную лист для хранения событий
events = []

# Нужна функция для загрузки из файла
def load_events():
    global events
    # try-except
    try:
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        events = []

# Сохранения событий
def save_events():
    global events
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=4)

# Запуск обратного отсчета
def start_timer():
    event_name = event_name_entry.get().strip()
    event_date = event_date_entry.get().strip()
    event_time = event_time_entry.get().strip()

    if not event_name:
        messagebox.showerror("Ошибка","Введите название события")
        return

    #проверка валидности даты
    try:
        if event_time: event_datetime = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S")
        else:
            event_datetime = datetime.strptime(event_date, "%Y-%m-%d")
            event_datetime = event_datetime.replace(hour=0, minute=0, second=0)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите дату в формате YYYY-MM-DD и время в формате HH:MM:SS!")
        return

    # проверка на прошедшее событие
    if event_datetime <= datetime.now():
        messagebox.showerror("Ошибка", "Дата и время события должны быть в будущем!")
        return

    # Добавляем в список событие
    events.append({"name": event_name, "datetime": event_datetime.strftime("%Y-%m-%d %H:%M:%S")})
    save_events()
    update_even_list()
    messagebox.showinfo("Успех", f"Событие '{event_name}' добавлено!")

# Функция для обновления списка
def update_even_list():
    event_list.delete(0, tk.END)
    for event in events:
        event_datetime = datetime.strptime(event["datetime"], "%Y-%m-%d %H:%M:%S")
        remaining_time = event_datetime - datetime.now()
        days, seconds = divmod(remaining_time.total_seconds(), 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        event_list.insert(tk.END, f"{event['name']} - {int(days)}д {int(hours)}ч {int(minutes)}м {int(seconds)}с")

# Фоновая функция обновления таймера
def update_timers():
    while True:
        time.sleep(1)
        if events:
            update_even_list()

root = tk.Tk()
root.title("Таймер обратного отсчета")

tk.Label(root, text="Название события:").pack()
event_name_entry = tk.Entry(root, width=30)
event_name_entry.pack()

tk.Label(root, text="Дата события (YYYY-MM-DD):").pack()
event_date_entry = tk.Entry(root, width=30)
event_date_entry.pack()

tk.Label(root, text="Время события (HH:MM:SS, опционально):").pack()
event_time_entry = tk.Entry(root, width=30)
event_time_entry.pack()

add_event_button = tk.Button(root, text="Добавить событие", command=start_timer)
add_event_button.pack()

event_list = tk.Listbox(root, width=50, height=10)
event_list.pack()

load_events()
update_even_list()

threading.Thread(target=update_timers, daemon=True).start()

root.mainloop()