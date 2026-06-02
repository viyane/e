# news_scraper.py
# Scrapes live headlines from Hacker News

import requests
import csv
from bs4 import BeautifulSoup
from datetime import date

def scrape_headlines():
    url = "https://news.ycombinator.com"
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to download page")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    rows = soup.find_all("tr", class_="athing")
    for row in rows:
        title_tag = row.find("span", class_="titleline")
        if title_tag:
            a = title_tag.find("a")
            if a:
                headlines.append({
                    "title": a.text.strip(),
                    "url": a.get("href", ""),
                    "date": str(date.today())
                })
    return headlines

def categorise(headlines):
    categories = {
        "AI": ["ai", "gpt", "llm", "machine learning", "openai", "claude", "model"],
        "Python": ["python", "django", "flask", "pip"],
        "Tech": ["apple", "google", "microsoft", "github", "linux"],
        "Science": ["space", "nasa", "physics", "biology", "research"],
        "Other": []
    }
    for h in headlines:
        title_lower = h["title"].lower()
        h["category"] = "Other"
        for cat, keywords in categories.items():
            if cat == "Other":
                continue
            for kw in keywords:
                if kw in title_lower:
                    h["category"] = cat
                    break
    return headlines

def print_report(headlines):
    print("=" * 50)
    print(f"  Hacker News — {date.today()}")
    print("=" * 50)
    print(f"  Total headlines scraped: {len(headlines)}")
    print()
    cats = {}
    for h in headlines:
        cat = h["category"]
        if cat not in cats:
            cats[cat] = []
        cats[cat].append(h)
    for cat, items in cats.items():
        if cat == "Other":
            continue
        print(f"--- {cat} ({len(items)}) ---")
        for h in items:
            print(f"  {h['title'][:55]}")
        print()
    print(f"--- Other ({len(cats.get('Other', []))}) ---")
    print(f"  {len(cats.get('Other', []))} uncategorised headlines")

def save_csv(headlines):
    filename = f"headlines_{date.today()}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "url", "category", "date"])
        writer.writeheader()
        writer.writerows(headlines)
    print()
    print(f"Saved to {filename}")
    return filename

headlines = scrape_headlines()
headlines = categorise(headlines)
print_report(headlines)
save_csv(headlines)