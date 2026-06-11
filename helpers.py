# helpers.py

def format_temp(temp):
    if temp > 30:
        feeling = "hot"
    elif temp > 20:
        feeling = "warm"
    elif temp > 10:
        feeling = "cool"
    else:
        feeling = "cold"
    return f"{temp}°C — feels {feeling}"

def format_wind(speed):
    if speed > 50:
        level = "strong"
    elif speed > 20:
        level = "moderate"
    else:
        level = "light"
    return f"{speed} km/h ({level})"

def divider(title):
    print(f"\n{'='*40}")
    print(f"  {title}")
    print(f"{'='*40}")