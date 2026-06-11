# main.py

from helpers import format_temp, format_wind, divider
from weather import get_weather, get_multiple

cities = [
    {"name": "Bengaluru", "lat": 12.97, "lon": 77.59},
    {"name": "Mumbai",    "lat": 19.07, "lon": 72.87},
    {"name": "Delhi",     "lat": 28.61, "lon": 77.20},
]

divider("Live Weather Dashboard")

results = get_multiple(cities)

for w in results:
    print(f"\n  {w['city']}")
    print(f"  Temp : {format_temp(w['temp'])}")
    print(f"  Wind : {format_wind(w['wind'])}")
    print(f"  Rain : {w['rain']}mm")

divider("Hourly forecast — Bengaluru")
bengaluru = get_weather("Bengaluru", 12.97, 77.59)
if bengaluru:
    hours = bengaluru["hourly"]
    for i, temp in enumerate(hours):
        bar = "█" * int(temp / 5)
        print(f"  Hour {i+1}: {temp}°C {bar}")

divider("Hottest city today")
if results:
    hottest = max(results, key=lambda w: w["temp"])
    print(f"  {hottest['city']} at {format_temp(hottest['temp'])}")

print("\nDone!")