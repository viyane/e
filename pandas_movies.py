# pandas_movies.py

import pandas as pd

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

df = pd.DataFrame(movies)

print("=== First 5 rows ===")
print(df.head())

print(f"\n=== Shape ===")
print(f"  {df.shape[0]} rows, {df.shape[1]} columns")

print("\n=== All Sci-Fi movies ===")
scifi = df[df["genre"] == "Sci-Fi"]
print(scifi[["title", "rating"]])

print("\n=== Top rated (9+), sorted ===")
top = df[df["rating"] >= 9].sort_values("rating", ascending=False)
print(top[["title", "rating", "year"]])

print("\n=== Average rating by genre ===")
avg_by_genre = df.groupby("genre")["rating"].mean().sort_values(ascending=False)
print(avg_by_genre)

print("\n=== Movie count by genre ===")
print(df.groupby("genre").size())

print("\n=== Overall stats ===")
print(f"  Average rating: {df['rating'].mean():.1f}")
print(f"  Highest rated:  {df.loc[df['rating'].idxmax(), 'title']}")
print(f"  Longest movie:  {df.loc[df['runtime'].idxmax(), 'title']} ({df['runtime'].max()} min)")
print(f"  Newest movie:   {df.loc[df['year'].idxmax(), 'title']} ({df['year'].max()})")

print("\n=== Decade column (new!) ===")
df["decade"] = (df["year"] // 10) * 10
print(df[["title", "year", "decade"]])

print("\n=== Movies per decade ===")
print(df.groupby("decade").size())

# save results
df.to_csv("movies_analysis.csv", index=False)
top.to_csv("top_rated.csv", index=False)
df.to_excel("movies.xlsx", index=False)

print("\nSaved: movies_analysis.csv, top_rated.csv, movies.xlsx")