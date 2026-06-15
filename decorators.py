# decorators.py

import functools
import time
from datetime import datetime


# --- 1. timer decorator ---

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"  [{func.__name__}] took {end-start:.3f}s")
        return result
    return wrapper


# --- 2. log decorator ---

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"  [{datetime.now():%H:%M:%S}] calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  [{datetime.now():%H:%M:%S}] {func.__name__} returned {result}")
        return result
    return wrapper


# --- 3. retry decorator ---

def retry(times=3, delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  Attempt {attempt+1} failed: {e}")
                    if attempt < times - 1:
                        time.sleep(delay)
            raise Exception(f"{func.__name__} failed after {times} attempts")
        return wrapper
    return decorator


# --- 4. validate_positive decorator ---

def validate_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if isinstance(arg, (int, float)) and arg < 0:
                raise ValueError(f"Negative value not allowed: {arg}")
        return func(*args, **kwargs)
    return wrapper


# --- apply them ---

@timer
def slow_calculation(n):
    time.sleep(0.1)
    return sum(range(n))

@log
def add(a, b):
    return a + b

@validate_positive
def square_root(n):
    return n ** 0.5

@retry(times=3, delay=0.1)
def flaky_function():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network blip!")
    return "success!"

@timer
@log
def stacked(n):
    time.sleep(0.05)
    return n * 2


# --- run everything ---

print("=== Timer ===")
result = slow_calculation(1000000)
print(f"  result: {result}")

print()
print("=== Logger ===")
add(10, 25)

print()
print("=== Validate ===")
print(f"  sqrt(16) = {square_root(16)}")
try:
    square_root(-4)
except ValueError as e:
    print(f"  caught: {e}")

print()
print("=== Retry ===")
try:
    result = flaky_function()
    print(f"  result: {result}")
except Exception as e:
    print(f"  gave up: {e}")

print()
print("=== Stacked decorators ===")
stacked(21)