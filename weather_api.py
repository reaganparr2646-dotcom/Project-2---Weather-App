import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherAPIError(Exception):
    """Custom exception for Weather API errors."""

def get_coordinates(city: str) -> dict:
    city = city.strip()

    if not city:
        raise WeatherAPIError("Please enter a city")


    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as e:
        raise WeatherAPIError(f"Error fetching coordinates for {city}: {e}") from e

    results = data.get("results")

    if not results:
        raise WeatherAPIError(f"No coordinates found for {city}")
    
    location = results[0]

    return {
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
        "name": location.get("name"),
        "state": location.get("admin1"),
        "country": location.get("country")
    }

def get_weather_description(code: int) -> str:
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Heavy drizzle",
        56: "Light freezing drizzle",
        57: "Heavy freezing drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Light rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        85: "Light snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with light hail",
        99: "Thunderstorm with heavy hail",
    }

    return weather_codes.get(code, "Unknown weather condition")

def get_current_weather(city: str) -> dict:

    location = get_coordinates(city)

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "current":(
            "temperature_2m,"
            "apparent_temperature,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
        "timezone": "auto"
    }

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

    except requests.RequestException as e:
        raise WeatherAPIError(f"Error fetching weather data for {city}: {e}") from e
    
    current = data.get("current")

    if not current:
        raise WeatherAPIError(f"No current weather data found for {city}")
    
    location_info = [
        location["name"],
        location["state"],
        location["country"]
    ]

    display_name = ",".join( part for part in location_info if part)

    return {
        "location": display_name,
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "weather_description": get_weather_description(current["weather_code"])
    }

