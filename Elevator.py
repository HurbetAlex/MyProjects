import tkinter as tk
import random
from tkinter import messagebox
import time
import threading
import queue

class ElevatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Elevator Simulation")
        self.floors = 4
        self.elevator_requests = queue.Queue(maxsize=10)
        self.current_floor = 1
        self.moving = False
        self.max_requests = 10
        self.request_timeout = 5
        self.random_occupants = True
        self.random_interval = 10

        self.build_ui()
        self.start_random_occupants()

    def build_ui(self):
        self.building_frame = tk.Frame(self.root)
        self.building_frame.pack(side=tk.LEFT, padx=10)

        self.elevator_frame = tk.Frame(self.building_frame)
        self.elevator_frame.pack()

        self.floors_ui = []
        for floor in range(self.floors, 0, -1):
            frame = tk.Frame(self.elevator_frame)
            frame.pack(fill=tk.X, pady=5)
            label = tk.Label(frame, text=f"Floor {floor}", width=10)
            label.pack(side=tk.LEFT)
            up_button = tk.Button(frame, text="Up", command=lambda f=floor: self.call_elevator(f, "up"))
            down_button = tk.Button(frame, text="Down", command=lambda f=floor: self.call_elevator(f, "down"))
            if floor == self.floors:
                down_button.pack(side=tk.RIGHT)
            elif floor == 1:
                up_button.pack(side=tk.RIGHT)
            else:
                up_button.pack(side=tk.RIGHT)
                down_button.pack(side=tk.RIGHT)
            self.floors_ui.append(frame)

        self.elevator_box = tk.Label(self.elevator_frame, text="Elevator", bg="gray", width=10, height=2)
        self.elevator_box.pack()

        self.control_panel_frame = tk.Frame(self.root)
        self.control_panel_frame.pack(side=tk.RIGHT, padx=10)

        self.control_label = tk.Label(self.control_panel_frame, text="Control Panel")
        self.control_label.pack()

        for floor in range(1, self.floors + 1):
            button = tk.Button(self.control_panel_frame, text=f"Floor {floor}", command=lambda f=floor: self.add_request(f))
            button.pack(pady=5)

        self.status_label = tk.Label(self.root, text="Status: Idle", fg="green")
        self.status_label.pack()

    def call_elevator(self, floor, direction):
        if self.elevator_requests.full():
            messagebox.showwarning("Warning", "Elevator request queue is full!")
            return
        self.elevator_requests.put((floor, direction))
        self.update_status()

    def add_request(self, floor):
        if self.elevator_requests.full():
            messagebox.showwarning("Warning", "Elevator request queue is full!")
            return
        self.elevator_requests.put((floor, None))
        self.update_status()

    def move_elevator(self, target_floor):
        self.moving = True
        while self.current_floor != target_floor:
            time.sleep(1)
            self.current_floor += 1 if self.current_floor < target_floor else -1
            self.update_elevator_position()
        time.sleep(2)
        self.moving = False

    def update_elevator_position(self):
        for i, frame in enumerate(self.floors_ui):
            bg_color = "gray" if self.floors - i == self.current_floor else "white"
            self.elevator_box.config(bg=bg_color)
            self.root.update_idletasks()

    def process_requests(self):
        while True:
            if not self.elevator_requests.empty() and not self.moving:
                floor, direction = self.elevator_requests.get()
                self.move_elevator(floor)
            elif not self.moving and self.current_floor != 1:
                self.move_elevator(1)
            time.sleep(1)

    def update_status(self):
        status = f"Requests: {self.elevator_requests.qsize()} / {self.max_requests}"
        self.status_label.config(text=status)

    def start_random_occupants(self):
        def random_arrival():
            while self.random_occupants:
                floor = random.randint(1, self.floors)
                direction = "up" if floor < self.floors else "down"
                self.call_elevator(floor, direction)
                time.sleep(self.random_interval)

        threading.Thread(target=random_arrival, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ElevatorApp(root)
    threading.Thread(target=app.process_requests, daemon=True).start()
    root.mainloop()
