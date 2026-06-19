# app.py

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

movies = [
    {"id": 1, "title": "Inception", "genre": "Sci-Fi", "rating": 9},
    {"id": 2, "title": "The Dark Knight", "genre": "Action", "rating": 10},
    {"id": 3, "title": "Interstellar", "genre": "Sci-Fi", "rating": 9},
    {"id": 4, "title": "Parasite", "genre": "Thriller", "rating": 8},
    {"id": 5, "title": "Dune", "genre": "Sci-Fi", "rating": 8},
]


@app.route("/")
def home():
    return render_template("index.html", movies=movies)


@app.route("/movie/<int:id>")
def movie(id):
    m = next((m for m in movies if m["id"] == id), None)
    if not m:
        return render_template("404.html"), 404
    return render_template("movie.html", movie=m)


@app.route("/genre/<genre>")
def by_genre(genre):
    filtered = [m for m in movies if m["genre"].lower() == genre.lower()]
    return render_template("genre.html", genre=genre, movies=filtered)


@app.route("/api/movies")
def api_movies():
    genre = request.args.get("genre")
    rating = request.args.get("min_rating", type=int)
    result = movies
    if genre:
        result = [m for m in result if m["genre"].lower() == genre.lower()]
    if rating:
        result = [m for m in result if m["rating"] >= rating]
    return jsonify(result)


@app.route("/api/movies/<int:id>")
def api_movie(id):
    m = next((m for m in movies if m["id"] == id), None)
    if not m:
        return jsonify({"error": "not found"}), 404
    return jsonify(m)


if __name__ == "__main__":
    app.run(debug=True)