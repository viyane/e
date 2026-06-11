# bookshop.py

import requests
import csv
from bs4 import BeautifulSoup

url = "http://books.toscrape.com"
response = requests.get(url)

print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

books = []

articles = soup.find_all("article")
for article in articles:
    title = article.find("h3").find("a")["title"]
    price = article.find("p", class_="price_color").text
    rating = article.find("p", class_="star-rating")["class"][1]
    books.append({
        "title": title,
        "price": price,
        "rating": rating
    })

print(f"\nScraped {len(books)} books")
print()

print("=== All books ===")
for b in books:
    print(f"  {b['title'][:40]} — {b['price']} ({b['rating']} stars)")

print()
print("=== Books under £15 ===")
for b in books:
    price_num = float(b["price"].replace("£", "").replace("Â", ""))
    if price_num < 15:
        print(f"  {b['title'][:40]} — {b['price']}")

print()
with open("books.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
    writer.writeheader()
    writer.writerows(books)

print(f"Saved {len(books)} books to books.csv")