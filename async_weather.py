# async_weather.py

import asyncio
import aiohttp
import time


CITIES = [
    {"name": "Bengaluru", "lat": 12.97, "lon": 77.59},
    {"name": "Mumbai",    "lat": 19.07, "lon": 72.87},
    {"name": "Delhi",     "lat": 28.61, "lon": 77.20},
    {"name": "London",    "lat": 51.50, "lon": -0.12},
    {"name": "Tokyo",     "lat": 35.68, "lon": 139.69},
]

URL = "https://api.open-meteo.com/v1/forecast"


async def fetch_weather(session, city):
    params = {
        "latitude": city["lat"],
        "longitude": city["lon"],
        "current": "temperature_2m,wind_speed_10m",
    }
    try:
        async with session.get(URL, params=params) as response:
            data = await response.json()
            temp = data["current"]["temperature_2m"]
            wind = data["current"]["wind_speed_10m"]
            return {"city": city["name"], "temp": temp, "wind": wind}
    except Exception as e:
        return {"city": city["name"], "error": str(e)}


async def fetch_all_async():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather(session, city) for city in CITIES]
        return await asyncio.gather(*tasks)


def fetch_all_sync():
    import requests
    results = []
    for city in CITIES:
        params = {
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current": "temperature_2m,wind_speed_10m",
        }
        try:
            r = requests.get(URL, params=params)
            data = r.json()
            temp = data["current"]["temperature_2m"]
            wind = data["current"]["wind_speed_10m"]
            results.append({"city": city["name"], "temp": temp, "wind": wind})
        except Exception as e:
            results.append({"city": city["name"], "error": str(e)})
    return results


def print_results(results):
    for r in results:
        if "error" in r:
            print(f"  {r['city']}: ERROR — {r['error']}")
        else:
            feeling = "hot" if r["temp"] > 30 else "warm" if r["temp"] > 20 else "cool"
            print(f"  {r['city']:<12} {r['temp']}°C ({feeling}), wind {r['wind']} km/h")


# --- sync timing ---
print("=== Synchronous (one at a time) ===")
start = time.time()
sync_results = fetch_all_sync()
sync_time = time.time() - start
print_results(sync_results)
print(f"  Time: {sync_time:.2f}s")

# --- async timing ---
print("\n=== Async (all at once) ===")
start = time.time()
async_results = asyncio.run(fetch_all_async())
async_time = time.time() - start
print_results(async_results)
print(f"  Time: {async_time:.2f}s")

# --- comparison ---
print(f"\n=== Result ===")
print(f"  Sync:  {sync_time:.2f}s")
print(f"  Async: {async_time:.2f}s")
print(f"  Async was {sync_time/async_time:.1f}x faster")