import tkinter as tk
from tkinter import messagebox, ttk

from weather_api import get_current_weather, WeatherAPIError

def get_weather(root, weather_info_frame):
    select_city_window = tk.Toplevel(root)

    select_city_window.title("Select City")
    select_city_window.geometry("200x200")
    select_city_window.resizable(False, False)

    ttk.Label(
        select_city_window,
        text="Enter a city name:",
    ).pack(
        anchor="w", padx=10, pady=10
    )

    city_entry = ttk.Entry(select_city_window)
    city_entry.pack(anchor="w", padx=10, pady=5)

    def clear_weather_results():
        for widget in weather_info_frame.winfo_children():
            widget.destroy()

    def submit_city():
        city = city_entry.get().strip()

        if not city:
            messagebox.showerror(
                "Error", 
                "Please enter a city name."
            )
            return
        
        weather_data = get_current_weather(city)

        clear_weather_results()
        display_weather_info(weather_info_frame, weather_data)
        select_city_window.destroy()
    Submit_button = ttk.Button(
        select_city_window,
        text="Submit",
        command=submit_city
    ).pack(pady=10)

    city_entry.focus()

def display_weather_info(weather_info_frame, weather_data):
    heading = ttk.Label(
        weather_info_frame,
        text=f"Current weather in {weather_data['location']}:",
        font=("Helvetica", 14, "bold")
    ).pack(anchor="w", padx=10, pady=5)

    if not weather_data:
        empty_label = ttk.Label(
            weather_info_frame,
            text="No weather data available.",
            font=("Helvetica", 12, "italic")
        ).pack(anchor="w", padx=10, pady=5)
        return
    
    weather_labels = [
        f"Temperature: {weather_data['temperature']}°F",
        f"Apparent Temperature: {weather_data['feels_like']}°F",
        f"Humidity: {weather_data['humidity']}%",
        f"Conditions: {weather_data['weather_description']}",
        f"Wind Speed: {weather_data['wind_speed']} mph"
    ]

    for label_text in weather_labels:
        ttk.Label(
            weather_info_frame,
            text=label_text,
            font=("Helvetica", 12)
        ).pack(anchor="w", padx=10, pady=2)

def main():
    root = tk.Tk()
    root.title("Weather Info")
    root.geometry("600x500")
    root.minsize(300,300)

    title_label = ttk.Label(
        root, text = "Weather Info", font=("Helvetica", 16, "bold")
    )
    title_label.pack(pady=10)

    weather_info_frame = ttk.Frame(root, padding=20)

    weather_button = ttk.Button(
        root, text="Enter a City", command=lambda: get_weather(root, weather_info_frame)
    )
    weather_button.pack(pady=10)

    weather_info_frame.pack(pady=10, fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()