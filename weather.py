# weather.py

import requests

def get_weather(city, lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,wind_speed_10m,precipitation,weather_code",
        "hourly": "temperature_2m",
        "forecast_days": 1
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "city": city,
            "temp": data["current"]["temperature_2m"],
            "wind": data["current"]["wind_speed_10m"],
            "rain": data["current"]["precipitation"],
            "hourly": data["hourly"]["temperature_2m"][:6]
        }
    except requests.exceptions.ConnectionError:
        print(f"No internet connection")
        return None
    except requests.exceptions.Timeout:
        print(f"Request timed out")
        return None

def get_multiple(cities):
    results = []
    for city in cities:
        w = get_weather(city["name"], city["lat"], city["lon"])
        if w:
            results.append(w)
    return results