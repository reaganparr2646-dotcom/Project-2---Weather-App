from weather_api import get_current_weather, WeatherAPIError

def main() -> None:
    city = input("Enter a city name: ")

    try:
        weather_data = get_current_weather(city)
        print(f"Current weather in {weather_data['location']}:")
        print(f"Temperature: {weather_data['temperature']}°F")
        print(f"Apparent Temperature: {weather_data['feels_like']}°F")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Conditions: {weather_data['weather_description']}")
        print(f"Wind Speed: {weather_data['wind_speed']} mph")

    except WeatherAPIError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()