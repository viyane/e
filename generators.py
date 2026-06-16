# generators.py

from itertools import islice


# --- 1. basic counter ---

def count_up(start, end):
    for i in range(start, end + 1):
        yield i


# --- 2. filter generator ---

def even_numbers(limit):
    for n in range(limit):
        if n % 2 == 0:
            yield n


# --- 3. infinite fibonacci ---

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


# --- 4. pipeline generators ---

def uppercase(gen):
    for item in gen:
        yield item.upper()

def with_numbers(gen):
    for i, item in enumerate(gen, 1):
        yield f"{i}. {item}"


# --- 5. read file with generator ---

def read_headlines(filename):
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if line:
                    yield line
    except FileNotFoundError:
        yield "file not found"


# --- run everything ---

print("=== Counter ===")
for n in count_up(1, 5):
    print(f"  {n}", end=" ")
print()

print("\n=== Even numbers under 20 ===")
print(f"  {list(even_numbers(20))}")

print("\n=== Fibonacci (first 10) ===")
print(f"  {list(islice(fibonacci(), 10))}")

print("\n=== Generator expression ===")
total = sum(x**2 for x in range(1, 11))
print(f"  Sum of squares 1-10: {total}")

print("\n=== List vs generator ===")
sq_list = [x**2 for x in range(5)]
sq_gen = (x**2 for x in range(5))
print(f"  list:      {sq_list}")
print(f"  generator: {sq_gen}")
print(f"  as list:   {list(sq_gen)}")

print("\n=== Pipeline ===")
headlines = ["breaking news today", "tech update", "sports results"]
pipeline = with_numbers(uppercase(iter(headlines)))
for line in pipeline:
    print(f"  {line}")

print("\n=== Read news.txt ===")
for i, line in enumerate(read_headlines("news.txt"), 1):
    print(f"  {i}: {line[:50]}")
    if i >= 3:
        print("  ...")
        break