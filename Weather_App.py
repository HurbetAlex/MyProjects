import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

API_KEY = "Mch5toSemGwo9vW1Fj1UG6J5vj2f5R2t"
BASE_URL = "http://dataservice.accuweather.com"

CITY_FILE = "last_city.json"


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")

        self.city_label = ttk.Label(root, text="Enter City:")
        self.city_label.pack(pady=5)

        self.city_entry = ttk.Entry(root, width=30)
        self.city_entry.pack(pady=5)
        self.city_entry.bind("<Return>", self.get_weather)

        self.weather_label = ttk.Label(root, text="", font=("Arial", 14))
        self.weather_label.pack(pady=10)

        self.icon_label = ttk.Label(root)
        self.icon_label.pack(pady=5)

        self.load_last_city()

    def save_last_city(self, city):
        with open(CITY_FILE, "w") as file:
            json.dump({"last_city": city}, file)

    def load_last_city(self):
        if os.path.exists(CITY_FILE):
            with open(CITY_FILE, "r") as file:
                data = json.load(file)
                city = data.get("last_city")
                if city:
                    self.city_entry.insert(0, city)
                    self.get_weather()

    def get_weather(self, event=None):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        location_url = f"{BASE_URL}/locations/v1/cities/search"
        params = {"apikey": API_KEY, "q": city}
        try:
            response = requests.get(location_url, params=params)
            response.raise_for_status()
            location_data = response.json()
            if not location_data:
                messagebox.showerror("Error", "City not found.")
                return
            city_key = location_data[0]["Key"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch city data: {e}")
            return

        weather_url = f"{BASE_URL}/currentconditions/v1/{city_key}"
        params = {"apikey": API_KEY, "details": "true"}
        try:
            response = requests.get(weather_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            if not weather_data:
                messagebox.showerror("Error", "Weather data not found.")
                return

            weather = weather_data[0]
            temperature = weather["Temperature"]["Metric"]["Value"]
            weather_text = weather["WeatherText"]
            is_daytime = weather["IsDayTime"]

            icon = weather["WeatherIcon"]
            icon_url = f"https://developer.accuweather.com/sites/default/files/{icon:02}-s.png"

            self.weather_label.config(
                text=f"Temperature: {temperature}°C\nCondition: {weather_text}"
            )
            self.icon_label.config(image="")
            icon_image = tk.PhotoImage(file=f"icon_{icon}.png")
            self.icon_label.image = icon_image

            self.save_last_city(city)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
