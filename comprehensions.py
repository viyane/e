# comprehensions.py

movies = [
    {"title": "Inception", "genre": "Sci-Fi", "rating": 9, "year": 2010, "runtime": 148},
    {"title": "The Dark Knight", "genre": "Action", "rating": 10, "year": 2008, "runtime": 152},
    {"title": "Interstellar", "genre": "Sci-Fi", "rating": 9, "year": 2014, "runtime": 169},
    {"title": "Parasite", "genre": "Thriller", "rating": 8, "year": 2019, "runtime": 132},
    {"title": "Dune", "genre": "Sci-Fi", "rating": 8, "year": 2021, "runtime": 155},
    {"title": "The Godfather", "genre": "Drama", "rating": 10, "year": 1972, "runtime": 175},
    {"title": "Joker", "genre": "Thriller", "rating": 7, "year": 2019, "runtime": 122},
    {"title": "Oppenheimer", "genre": "Drama", "rating": 9, "year": 2023, "runtime": 180},
    {"title": "Arrival", "genre": "Sci-Fi", "rating": 8, "year": 2016, "runtime": 116},
    {"title": "The Matrix", "genre": "Action", "rating": 9, "year": 1999, "runtime": 136},
]

# 1. list of all titles 
titles = [m["title"] for m in movies]
print("=== All titles ===")
print(titles)

# 2. only top rated 9+
top_rated = [m["title"] for m in movies if m["rating"] >= 9]
print("n==== Top rated (9+) ====")
print(top_rated)

# 3. only sci-fi movies
scifi = [m for m in movies if m["genre"] == "Sci-Fi"]
print("\n==== Runtimes in hours ====")
for m in scifi:
    print(f"  {m['title']} ({m['year']})")

# 4. runtime in hours using comprehension
runtimes = {m["title"]: round(m["runtime"] / 60, 1) for m in movies}
print("\n=== Runtimes in hours ===")
for title, hours in runtimes.items():
    print(f"  {title}: {hours}h")

# 5. unique genres using set comprehension
genres = {m["genre"] for m in movies}
print("\n=== Unique genres ===")
print(genres)

# 6. movies grouped by genre using dict comprehension
genre_counts = {genre: len([m for m in movies if m["genre"] == genre]) for genre in genres}
print("\n=== Movies per genre ===")
for genre, count in sorted(genre_counts.items()):
    print(f"  {genre}: {count}")

# 7. long movies over 2.5 hours, top rated only
epic_top = [m["title"] for m in movies if m["runtime"] > 150 and m["rating"] >= 9]
print("\n=== Epic top-rated films (150+ min, rating 9+) ===")
print(epic_top)

# 8. average rating using comprehension
ratings = [m["rating"] for m in movies]
avg = sum(ratings) / len(ratings)
print(f"\n=== Average rating: {avg:.1f} ===")