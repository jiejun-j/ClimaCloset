from urllib.parse import urlencode
from dotenv import load_dotenv
import os


# Get the API key from the environment variables.
load_dotenv()
API_KEY: str = os.getenv("KEY")


# A dictionary mapping different weather conditions to their respective image sources.
# For simplicity, multiple weather conditions are mapped to the 'mist.png' image.
WEATHER_IMAGE_MAP = {
    "thunderstorm": "/thunderstorm.png",
    "drizzle": "/drizzle.png",
    "rain": "/rain.png",
    "snow": "/snow.png",
    "clear": "/clear.png",
    "clouds": "/clouds.png",
    "mist": "/mist.png",
    "smoke": "/mist.png",
    "haze": "/mist.png",
    "dust": "/mist.png",
    "fog": "/mist.png",
    "sand": "/mist.png",
    "ash": "/mist.png",
    "squalls": "/mist.png",
    "tornado": "/mist.png",
}


# API request: Constructs the URL based on the given city name.
def get_weather_request(city: str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    query_parameters = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    encoded_parameters = urlencode(query_parameters)
    full_url = f"{base_url}?{encoded_parameters}"

    return full_url