from flask import Flask, render_template, jsonify, request
import requests
import sqlite3
import os
from config import OMDB_API_KEY

app = Flask(__name__)

OMDB_URL = "http://www.omdbapi.com/"
TITLES = ["Inception", "The Dark Knight", "Interstellar", "Parasite", "Dune"]
DB_FILE = "movies_cache.db"


def fetch_movie(title):
    params = {"t": title, "apikey": OMDB_API_KEY}
    response = requests.get(OMDB_URL, params=params, timeout=10)
    return response.json()


def setup_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            genre TEXT,
            rating TEXT,
            year TEXT,
            poster TEXT,
            plot TEXT
        )
    """)


def get_movies():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        setup_db(conn)
        rows = conn.execute("SELECT * FROM movies").fetchall()

        if not rows:
            print("Cache empty — fetching from OMDb...")
            for title in TITLES:
                data = fetch_movie(title)
                if data.get("Response") == "True":
                    conn.execute(
                        "INSERT INTO movies (title, genre, rating, year, poster, plot) VALUES (?,?,?,?,?,?)",
                        (
                            data.get("Title"),
                            data.get("Genre", "").split(", ")[0],
                            data.get("imdbRating"),
                            data.get("Year"),
                            data.get("Poster"),
                            data.get("Plot"),
                        )
                    )
            conn.commit()
            rows = conn.execute("SELECT * FROM movies").fetchall()

        return [dict(row) for row in rows]


@app.route("/")
def home():
    movies = get_movies()
    return render_template("index.html", movies=movies)


@app.route("/movie/<int:id>")
def movie(id):
    movies = get_movies()
    m = next((m for m in movies if m["id"] == id), None)
    if not m:
        return render_template("404.html"), 404
    return render_template("movie.html", movie=m)


@app.route("/genre/<genre>")
def by_genre(genre):
    movies = get_movies()
    filtered = [m for m in movies if m["genre"].lower() == genre.lower()]
    return render_template("genre.html", genre=genre, movies=filtered)


@app.route("/api/movies")
def api_movies():
    movies = get_movies()
    genre = request.args.get("genre")
    if genre:
        movies = [m for m in movies if m["genre"].lower() == genre.lower()]
    return jsonify(movies)


@app.route("/refresh")
def refresh():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    return "Cache cleared! Visit / to refetch from OMDb."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)