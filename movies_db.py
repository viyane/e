# movies_db.py

import sqlite3

movies = [
    ("Inception", "Sci-Fi", 9, 2010, 148),
    ("The Dark Knight", "Action", 10, 2008, 152),
    ("Interstellar", "Sci-Fi", 9, 2014, 169),
    ("Parasite", "Thriller", 8, 2019, 132),
    ("Dune", "Sci-Fi", 8, 2021, 155),
    ("The Godfather", "Drama", 10, 1972, 175),
    ("Joker", "Thriller", 7, 2019, 122),
    ("Oppenheimer", "Drama", 9, 2023, 180),
    ("Arrival", "Sci-Fi", 8, 2016, 116),
    ("The Matrix", "Action", 9, 1999, 136),
]


def setup(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            genre TEXT,
            rating INTEGER,
            year INTEGER,
            runtime INTEGER
        )
    """)


def seed(conn):
    conn.execute("DELETE FROM movies")
    conn.executemany(
        "INSERT INTO movies (title, genre, rating, year, runtime) VALUES (?,?,?,?,?)",
        movies
    )


def all_movies(conn):
    return conn.execute("SELECT title, genre, rating FROM movies ORDER BY rating DESC").fetchall()


def by_genre(conn, genre):
    return conn.execute(
        "SELECT title, rating FROM movies WHERE genre = ? ORDER BY rating DESC",
        (genre,)
    ).fetchall()


def top_rated(conn, min_rating):
    return conn.execute(
        "SELECT title, rating, year FROM movies WHERE rating >= ? ORDER BY rating DESC",
        (min_rating,)
    ).fetchall()


def stats(conn):
    count = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
    avg = conn.execute("SELECT AVG(rating) FROM movies").fetchone()[0]
    best = conn.execute("SELECT title FROM movies ORDER BY rating DESC LIMIT 1").fetchone()[0]
    longest = conn.execute("SELECT title, runtime FROM movies ORDER BY runtime DESC LIMIT 1").fetchone()
    return count, avg, best, longest


with sqlite3.connect("movies.db") as conn:
    setup(conn)
    seed(conn)

    print("=== All movies ===")
    for row in all_movies(conn):
        print(f"  {row[0]:<35} {row[1]:<12} {row[2]}/10")

    print("\n=== Sci-Fi movies ===")
    for row in by_genre(conn, "Sci-Fi"):
        print(f"  {row[0]} — {row[1]}/10")

    print("\n=== Top rated (9+) ===")
    for row in top_rated(conn, 9):
        print(f"  {row[0]} ({row[2]}) — {row[1]}/10")

    print("\n=== Stats ===")
    count, avg, best, longest = stats(conn)
    print(f"  Total movies   : {count}")
    print(f"  Average rating : {avg:.1f}")
    print(f"  Best movie     : {best}")
    print(f"  Longest film   : {longest[0]} ({longest[1]} mins)")