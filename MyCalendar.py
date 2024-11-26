import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import calendar
from datetime import datetime, timedelta
import json
import os


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Calendar")

        self.event_file = "events.json"
        self.events = self.load_events()

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.theme = "light"

        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(pady=10)

        self.prev_button = tk.Button(self.header_frame, text="<", command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.month_label = tk.Label(self.header_frame, text="", font=("Arial", 16))
        self.month_label.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(self.header_frame, text=">", command=self.next_month)
        self.next_button.pack(side=tk.LEFT, padx=10)

        self.theme_button = tk.Button(self.header_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side=tk.RIGHT, padx=10)

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack(pady=10)

        self.build_calendar()

    def load_events(self):
        if os.path.exists(self.event_file):
            with open(self.event_file, 'r') as f:
                return json.load(f)
        return {}

    def save_events(self):
        with open(self.event_file, 'w') as f:
            json.dump(self.events, f, indent=4)

    def build_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        days_frame = tk.Frame(self.calendar_frame)
        days_frame.pack()
        for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
            tk.Label(days_frame, text=day, width=10, borderwidth=1, relief="solid").pack(side=tk.LEFT)

        cal = calendar.Calendar()
        dates_frame = tk.Frame(self.calendar_frame)
        dates_frame.pack()

        for week in cal.monthdayscalendar(self.current_year, self.current_month):
            week_frame = tk.Frame(dates_frame)
            week_frame.pack()
            for day in week:
                day_button = tk.Button(week_frame, text=str(day) if day != 0 else "",
                                       width=10, height=3, command=lambda d=day: self.show_event_dialog(d))
                day_button.pack(side=tk.LEFT)
                if day != 0:
                    date_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    if date_key in self.events:
                        day_button.config(bg="lightblue")

    def show_event_dialog(self, day):
        if day == 0:
            return

        date_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        events = self.events.get(date_key, [])

        event_window = tk.Toplevel(self.root)
        event_window.title(f"Events for {date_key}")

        def add_event():
            event_text = simpledialog.askstring("Add Event", "Enter event details:")
            if event_text:
                events.append({"text": event_text, "reminder": None})
                self.events[date_key] = events
                self.save_events()
                self.build_calendar()
                event_window.destroy()

        def delete_event(index):
            if messagebox.askyesno("Delete Event", "Are you sure you want to delete this event?"):
                events.pop(index)
                if not events:
                    del self.events[date_key]
                else:
                    self.events[date_key] = events
                self.save_events()
                self.build_calendar()
                event_window.destroy()

        tk.Button(event_window, text="Add Event", command=add_event).pack(pady=5)
        for idx, event in enumerate(events):
            frame = tk.Frame(event_window)
            frame.pack(pady=5)
            tk.Label(frame, text=event["text"]).pack(side=tk.LEFT, padx=5)
            tk.Button(frame, text="Delete", command=lambda i=idx: delete_event(i)).pack(side=tk.RIGHT)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.build_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.build_calendar()

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        bg_color = "black" if self.theme == "dark" else "white"
        fg_color = "white" if self.theme == "dark" else "black"

        self.root.config(bg=bg_color)
        self.header_frame.config(bg=bg_color)
        self.calendar_frame.config(bg=bg_color)
        self.month_label.config(bg=bg_color, fg=fg_color)
        self.theme_button.config(bg=bg_color, fg=fg_color)

        for widget in self.calendar_frame.winfo_children():
            try:
                widget.config(bg=bg_color, fg=fg_color)
            except tk.TclError:
                widget.config(bg=bg_color)

        self.build_calendar()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
