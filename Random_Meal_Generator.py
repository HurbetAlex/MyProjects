import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import webbrowser

def fetch_random_meal():
    response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_meal():
    meal_data = fetch_random_meal()
    if meal_data:
        meal = meal_data["meals"][0]

        meal_name.set(meal["strMeal"])

        ingredients_text = ""
        for i in range(1, 21):
            ingredient = meal[f"strIngredient{i}"]
            measure = meal[f"strMeasure{i}"]
            if ingredient and ingredient.strip():
                ingredients_text += f"{measure} {ingredient}\n"

        instructions.set(meal["strInstructions"])

        image_url = meal["strMealThumb"]
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)
            meal_image = Image.open(image_data)
            meal_image = meal_image.resize((300, 300), Image.Resampling.LANCZOS)
            img = ImageTk.PhotoImage(meal_image)
            meal_image_label.configure(image=img)
            meal_image_label.image = img

        youtube_url.set(meal["strYoutube"])

def open_youtube():
    if youtube_url.get():
        webbrowser.open(youtube_url.get())

app = tk.Tk()
app.title("Random Meal Generator")
app.geometry("600x700")

meal_name = tk.StringVar()
meal_name_label = ttk.Label(app, textvariable=meal_name, font=("Helvetica", 16, "bold"))
meal_name_label.pack(pady=10)

meal_image_label = ttk.Label(app)
meal_image_label.pack(pady=10)

ingredients_frame = ttk.LabelFrame(app, text="Ingredients")
ingredients_frame.pack(fill="both", expand="yes", padx=10, pady=10)
ingredients = tk.StringVar()
ingredients_label = ttk.Label(ingredients_frame, textvariable=ingredients, justify="left")
ingredients_label.pack(pady=10, padx=10)

instructions_frame = ttk.LabelFrame(app, text="Instructions")
instructions_frame.pack(fill="both", expand="yes", padx=10, pady=10)
instructions = tk.StringVar()
instructions_label = ttk.Label(instructions_frame, textvariable=instructions, wraplength=350, justify="left")
instructions_label.pack(pady=10, padx=10)

youtube_url = tk.StringVar()
youtube_button = ttk.Button(app, text="Watch on Youtube", command=open_youtube)
youtube_button.pack(pady=10)

generate_button = ttk.Button(app, text="Generate Meal", command=display_meal())
generate_button.pack(pady=10)

display_meal()
app.mainloop()