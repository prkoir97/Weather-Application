from geopy.geocoders import Photon
from timezonefinder import TimezoneFinder
import pytz
import requests
import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk
import io
import numpy as np
import json
from config import api_key


def get_weather():
    city = entry_city.get()

    # Initialize geolocator and get location coordinates based on city name
    geolocator = Photon(user_agent="geoapiExercises")
    location = geolocator.geocode(city)

    if location is None:
        print("City not found")
        return

    # Find timezone of the location
    timezone_finder = TimezoneFinder()
    timezone = timezone_finder.timezone_at(lng=location.longitude, lat=location.latitude)
    timezone_label.config(text=timezone)

    # Update latitude and longitude labels
    latitude_longitude_label.config(text=f"{round(location.latitude, 4)}°N, {round(location.longitude, 4)}°E")

    # Convert the current time to the local time of the location
    local_time = datetime.now(pytz.timezone(timezone))
    current_time_label.config(text=local_time.strftime("%Y-%m-%d %H:%M:%S"))

    # Fetch weather data from OpenWeatherMap API
    # api_key imported from config.py
    api_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={location.latitude}&lon={location.longitude}&units=metric&exclude=hourly&appid={api_key}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        weather_data = response.json()

        # Extract current weather details
        current_weather = weather_data.get('current', {})
        temperature = current_weather.get('temp', 'N/A')
        humidity = current_weather.get('humidity', 'N/A')
        pressure = current_weather.get('pressure', 'N/A')
        wind_speed = current_weather.get('wind_speed', 'N/A')
        description = current_weather['weather'][0].get('description', 'N/A')

        # Update GUI labels with current weather details
        temperature_label.config(text=f"Temperature: {temperature}°C")
        humidity_label.config(text=f"Humidity: {humidity}%")
        pressure_label.config(text=f"Pressure: {pressure} hPa")
        wind_speed_label.config(text=f"Wind Speed: {wind_speed} m/s")
        description_label.config(text=f"Description: {description}")

        # Load weather icon for current weather
        icon_url = f"http://openweathermap.org/img/wn/{current_weather['weather'][0]['icon']}.png"
        response = requests.get(icon_url)
        if response.status_code == 200:
            icon_data = response.content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)

            weather_icon_label.config(image=icon_photo)
            weather_icon_label.image = icon_photo
        else:
            print("Failed to load weather icon for current weather")

        # Extract weather forecast for the next few days
        daily_forecast = weather_data.get('daily', [])
        forecast_data = []
        for day_data in daily_forecast:
            timestamp = day_data.get('dt', 0)
            day_of_week = datetime.fromtimestamp(timestamp).strftime('%A')
            date = day_of_week
            min_temp = day_data['temp'].get('min', 'N/A')
            max_temp = day_data['temp'].get('max', 'N/A')
            weather_desc = day_data['weather'][0].get('description', 'N/A')
            weather_icon = day_data['weather'][0].get('icon', '01d')  # Default icon code
            forecast_data.append({
                'date': date,
                'min_temp': min_temp,
                'max_temp': max_temp,
                'weather_desc': weather_desc,
                'weather_icon': weather_icon
            })

        # Store forecast data in a NumPy array for further processing
        forecast_array = np.array(forecast_data)

        # Save forecast data to a JSON file
        with open('weather_forecast.json', 'w') as f:
            json.dump(forecast_data, f, indent=4)

        # Display weather forecast for the week
        display_forecast(forecast_data, forecast_frame)

        print("Weather data fetched successfully")

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")

def display_forecast(forecast_data, forecast_frame):
    # Create a label frame for the forecast
    forecast_label_frame = tk.LabelFrame(forecast_frame, text="Weather Forecast")
    forecast_label_frame.pack(fill="both", expand=False)
    forecast_label_frame.config(bg="#add8e6")

    # Add labels and icons for each day's forecast
    for i, day_data in enumerate(forecast_data):
        date_label = tk.Label(forecast_label_frame, text=day_data['date'], bg="#add8e6")
        date_label.grid(row=i, column=0, padx=10, pady=5)

        min_temp_label = tk.Label(forecast_label_frame, text=f"Min Temp: {day_data['min_temp']}°C", bg="#add8e6")
        min_temp_label.grid(row=i, column=1, padx=10, pady=5)

        max_temp_label = tk.Label(forecast_label_frame, text=f"Max Temp: {day_data['max_temp']}°C", bg="#add8e6")
        max_temp_label.grid(row=i, column=2, padx=10, pady=5)

        weather_desc_label = tk.Label(forecast_label_frame, text=f"Weather: {day_data['weather_desc']}", bg="#add8e6")
        weather_desc_label.grid(row=i, column=3, padx=10, pady=5)

        # Load weather icon
        icon_url = f"http://openweathermap.org/img/wn/{day_data['weather_icon']}.png"
        response = requests.get(icon_url)
        if response.status_code == 200:
            icon_data = response.content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)

            icon_label = tk.Label(forecast_label_frame, image=icon_photo, bg="#add8e6")
            icon_label.image = icon_photo  # Keep a reference to the image to prevent garbage collection
            icon_label.grid(row=i, column=4, padx=10, pady=5)
        else:
            print(f"Failed to load weather icon for {day_data['date']}")

# Create the root window: set title, size and position, background color, non-resizable
root = tk.Tk()
root.title("Weather App")
root.configure(bg="#add8e6")

# Create input field
entry_city = tk.Entry(root, justify="center")
entry_city.pack()
#entry_city.focus()  # Focus

# Create a button to trigger weather fetching
button_get_weather = tk.Button(root, text="Get Weather", bg="#add8e6", command=get_weather)
button_get_weather.pack()

# Create labels to display current weather information
current_weather_frame = tk.LabelFrame(root, text="Today's Weather Report", bg="#add8e6", padx=10, pady=10)
current_weather_frame.pack(fill="both", expand=False)
current_weather_frame.config(bg="#add8e6")
#current_weather_frame.pack(padx=10, pady=10, fill="both", expand=False)

# Create labels to display current weather information
timezone_label = tk.Label(current_weather_frame, text="Timezone: ", bg="#add8e6")
timezone_label.pack()
latitude_longitude_label = tk.Label(current_weather_frame, text="Latitude, Longitude: ", bg="#add8e6")
latitude_longitude_label.pack()
current_time_label = tk.Label(current_weather_frame, text="Current Time: ", bg="#add8e6")
current_time_label.pack()
temperature_label = tk.Label(current_weather_frame, text="Temperature: ", bg="#add8e6")
temperature_label.pack()
humidity_label = tk.Label(current_weather_frame, text="Humidity: ", bg="#add8e6")
humidity_label.pack()
pressure_label = tk.Label(current_weather_frame, text="Pressure: ", bg="#add8e6")
pressure_label.pack()
wind_speed_label = tk.Label(current_weather_frame, text="Wind Speed: ", bg="#add8e6")
wind_speed_label.pack()
description_label = tk.Label(current_weather_frame, text="Description: ", bg="#add8e6")
description_label.pack()

# Load weather icon for current weather
weather_icon_label = tk.Label(current_weather_frame, bg="#add8e6")
weather_icon_label.pack()

# Create a frame to display weather forecast for the week
forecast_frame = tk.Frame(root)
forecast_frame.pack(pady=20)

# Run the GUI main loop
root.mainloop()
