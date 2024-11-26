import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math


class CorrelationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Correlation Calculator")

        self.data = []

        self.input_frame = ttk.Frame(root)
        self.input_frame.pack(pady=10)

        ttk.Label(self.input_frame, text="X:").grid(row=0, column=0, padx=5)
        self.x_entry = ttk.Entry(self.input_frame, width=10)
        self.x_entry.grid(row=0, column=1, padx=5)

        ttk.Label(self.input_frame, text="Y:").grid(row=0, column=2, padx=5)
        self.y_entry = ttk.Entry(self.input_frame, width=10)
        self.y_entry.grid(row=0, column=3, padx=5)

        ttk.Button(self.input_frame, text="Add", command=self.add_data).grid(row=0, column=4, padx=5)

        self.table_frame = ttk.Frame(root)
        self.table_frame.pack()

        self.data_table = ttk.Treeview(self.table_frame, columns=("X", "Y"), show="headings", height=10)
        self.data_table.heading("X", text="X")
        self.data_table.heading("Y", text="Y")
        self.data_table.pack()

        self.calculate_button = ttk.Button(root, text="Calculate", command=self.calculate, state="disabled")
        self.calculate_button.pack(pady=10)

        self.results_label = tk.Label(root, text="", justify="left", font=("Arial", 12))
        self.results_label.pack()

        ttk.Button(root, text="Load Data from File", command=self.load_data).pack(pady=5)

        ttk.Button(root, text="Show Scatter Plot", command=self.show_scatter_plot).pack(pady=5)

    def add_data(self):
        try:
            x = float(self.x_entry.get())
            y = float(self.y_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Both X and Y must be valid numbers.")
            return

        self.data.append((x, y))
        self.update_table()
        self.calculate_button.config(state="normal")

    def update_table(self):
        for row in self.data_table.get_children():
            self.data_table.delete(row)

        for i, (x, y) in enumerate(self.data, start=1):
            self.data_table.insert("", "end", iid=i, values=(x, y))

    def calculate(self):
        if not self.data:
            messagebox.showerror("No Data", "Add some data points first.")
            return

        x_vals = [point[0] for point in self.data]
        y_vals = [point[1] for point in self.data]

        x_mean = sum(x_vals) / len(x_vals)
        y_mean = sum(y_vals) / len(y_vals)

        x_std_dev = math.sqrt(sum((x - x_mean) ** 2 for x in x_vals) / len(x_vals))
        y_std_dev = math.sqrt(sum((y - y_mean) ** 2 for y in y_vals) / len(y_vals))

        if x_std_dev == 0 or y_std_dev == 0:
            messagebox.showerror("Calculation Error",
                                 "Standard deviation is zero for one or both variables. Correlation cannot be computed.")
            return

        covariance = sum((x - x_mean) * (y - y_mean) for x, y in self.data) / len(self.data)

        correlation = covariance / (x_std_dev * y_std_dev)

        interpretation = self.interpret_correlation(correlation)

        results = (
            f"X Mean: {x_mean:.2f}\n"
            f"Y Mean: {y_mean:.2f}\n"
            f"X Std Dev: {x_std_dev:.2f}\n"
            f"Y Std Dev: {y_std_dev:.2f}\n"
            f"Pearson Correlation: {correlation:.2f}\n"
            f"Interpretation: {interpretation}"
        )
        self.results_label.config(text=results)

    def interpret_correlation(self, correlation):
        if abs(correlation) < 0.1:
            return "No correlation"
        elif abs(correlation) < 0.3:
            return "Neutral"
        elif abs(correlation) < 0.7:
            return "Some correlation"
        else:
            return "Strong correlation"

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                for line in file:
                    x, y = map(float, line.strip().split(","))
                    self.data.append((x, y))
            self.update_table()
            self.calculate_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not load file: {e}")

    def show_scatter_plot(self):
        if not self.data:
            messagebox.showerror("No Data", "Add some data points first.")
            return

        x_vals = [point[0] for point in self.data]
        y_vals = [point[1] for point in self.data]

        x_mean = sum(x_vals) / len(x_vals)
        y_mean = sum(y_vals) / len(y_vals)

        slope = sum((x - x_mean) * (y - y_mean) for x, y in self.data) / sum((x - x_mean) ** 2 for x in x_vals)
        intercept = y_mean - slope * x_mean

        regression_line = [slope * x + intercept for x in x_vals]

        plt.figure(figsize=(8, 6))
        plt.scatter(x_vals, y_vals, label="Data Points")
        plt.plot(x_vals, regression_line, color="red", label="Regression Line")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.title("Scatter Plot with Regression Line")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = CorrelationApp(root)
    root.mainloop()
