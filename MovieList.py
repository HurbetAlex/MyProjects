import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import io

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Database App")
        self.api_key = "0bdf8f905c6825cc890df805ea4dda67"
        self.base_url = "https://api.themoviedb.org/3"
        self.poster_base_url = "https://image.tmdb.org/t/p/w200"
        self.current_page = 1
        self.movies = []

        self.setup_ui()
        self.load_movies()

    def setup_ui(self):
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.movie_list_frame = tk.Frame(self.main_frame)
        self.movie_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.movie_list_canvas = tk.Canvas(self.movie_list_frame)
        self.movie_list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.movie_list_frame, orient="vertical", command=self.movie_list_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.movie_list_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.movie_list_inner_frame = tk.Frame(self.movie_list_canvas)
        self.movie_list_canvas.create_window((0, 0), window=self.movie_list_inner_frame, anchor="nw")

        self.movie_list_inner_frame.bind("<Configure>", lambda e: self.movie_list_canvas.configure(scrollregion=self.movie_list_canvas.bbox("all")))

        self.detail_frame = tk.Frame(self.main_frame, bg="white", width=300)
        self.detail_frame.pack(side=tk.RIGHT, fill=tk.Y)

    def load_movies(self):
        url = f"{self.base_url}/movie/now_playing?api_key={self.api_key}&language=en-US&page={self.current_page}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            self.movies.extend(data["results"])
            self.display_movies()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to load movies: {e}")

    def display_movies(self):
        for movie in self.movies:
            frame = tk.Frame(self.movie_list_inner_frame, pady=5, padx=5, borderwidth=1, relief="solid")
            frame.pack(fill=tk.X, pady=5)

            poster_url = self.poster_base_url + movie.get("poster_path", "")
            poster_image = self.load_image(poster_url, (50, 75))

            if poster_image:
                poster_label = tk.Label(frame, image=poster_image)
                poster_label.image = poster_image
                poster_label.pack(side=tk.LEFT)

            movie_info_frame = tk.Frame(frame)
            movie_info_frame.pack(side=tk.LEFT, padx=10)

            title = movie.get("title", "N/A")
            release_date = movie.get("release_date", "N/A")
            tk.Label(movie_info_frame, text=title, font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(movie_info_frame, text=f"Release Date: {release_date}", font=("Arial", 10)).pack(anchor="w")

            tk.Button(frame, text="View Details", command=lambda m=movie: self.display_movie_details(m)).pack(side=tk.RIGHT)

    def display_movie_details(self, movie):
        for widget in self.detail_frame.winfo_children():
            widget.destroy()

        poster_url = self.poster_base_url + movie.get("poster_path", "")
        poster_image = self.load_image(poster_url, (150, 225))

        if poster_image:
            poster_label = tk.Label(self.detail_frame, image=poster_image, bg="white")
            poster_label.image = poster_image
            poster_label.pack()

        title = movie.get("title", "N/A")
        overview = movie.get("overview", "N/A")
        rating = movie.get("vote_average", "N/A")
        release_date = movie.get("release_date", "N/A")

        tk.Label(self.detail_frame, text=title, font=("Arial", 16, "bold"), bg="white").pack(anchor="w", pady=10)
        tk.Label(self.detail_frame, text=f"Rating: {rating}", font=("Arial", 12), bg="white").pack(anchor="w")
        tk.Label(self.detail_frame, text=f"Release Date: {release_date}", font=("Arial", 12), bg="white").pack(anchor="w")
        tk.Label(self.detail_frame, text="Overview:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=5)
        tk.Label(self.detail_frame, text=overview, wraplength=280, justify="left", bg="white").pack(anchor="w", pady=5)

    def load_image(self, url, size):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = Image.open(io.BytesIO(response.content))
            image_data = image_data.resize(size, Image.ANTIALIAS)
            return ImageTk.PhotoImage(image_data)
        except Exception:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
