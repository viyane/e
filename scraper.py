import csv
with open("books.csv", "w", newline="") as f:
writer = csv.DictWriter(f, fieldnames=["title", "price"])
writer.writeheader()
writer.writerows(books)
print(f"Saved {len(books)} books to books.csv")