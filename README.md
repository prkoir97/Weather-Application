## **Weather App**

This Weather App is a simple graphical interface built in Python using Tkinter, allowing users to fetch current weather information and forecast for a specified city. It fetches data from the OpenWeatherMap API and displays it in a user-friendly format.

### Usage

1. Input the desired city in the provided entry field.
2. Click the "Get Weather" button to fetch the weather data.
3. Current weather details and a weekly forecast will be displayed.

### Dependencies

This application relies on the following Python libraries:
- Geopy for geocoding and retrieving location coordinates.
- Timezonefinder for determining the timezone of a location.
- Requests for making HTTP requests to the OpenWeatherMap API.
- Pytz for handling timezones.
- Tkinter for creating the graphical user interface.
- PIL (Python Imaging Library) for working with images.
- NumPy for array manipulation.
- Json for handling JSON data.

### Acknowledgments

This Weather App was inspired by the tutorial provided by DataScientist from Udemy's highly rated course. Special thanks to DataScientist for the inspiration.

### Instructions

1. Install the required dependencies by running:
   
    `pip install geopy timezonefinder requests pillow numpy`

3. Obtain an API key from [OpenWeatherMap](https://openweathermap.org/api) and store it in a file named `config.py` with the variable `api_key`.
4. Run the provided Python script to launch the Weather App.

### Note

Ensure you have a stable internet connection to fetch weather data successfully.

