import reflex as rx
import requests
import asyncio
from weather_assistant.weather_data import get_weather_request, WEATHER_IMAGE_MAP
from weather_assistant.wardrobe_data import Items


# The State class keeps track of various attributes related to the user's input and the resulting weather data.
class State(rx.State):
    # Weather attributes
    location: str = ""
    city: str = ""
    country: str = ""
    temp: str = ""
    speed: str = ""
    humidity: str = ""
    weather_condition: str = ""
    image_src: str = ""
    
    # User input attributes
    user_input: str = ""
    
    # Content attributes
    clothing_advice: str = ""
    error_message: str = ""
    
    # Styling attributes
    content_height: str = "0px"
    content_bg: str = ""
    
    def get_input_value(self, user_input):
        self.user_input = user_input
    
    async def handle_key_press(self, key):
        if key == "Enter" and self.user_input != "":
            self.expand_content_height()
            await self.give_content_bg()
            await self.get_weather_data()
    
    async def give_content_bg(self):
        await asyncio.sleep(0.2)
        if self.content_bg != "#fafafa":
            self.content_bg = "#fafafa"
    
    def expand_content_height(self):
        if self.content_height != "250px":
            self.content_height = "250px"
            
    async def get_weather_data(self):
        response = requests.get(get_weather_request(self.user_input))
        await asyncio.sleep(0.05)
        
        if response.status_code == 200:
            data = response.json()
            
            self.city = self.user_input
            self.country = data["sys"]["country"]
            self.temp = f"{int(data['main']['temp'])}°C"
            self.humidity = f"{int(data['main']['humidity'])}%"
            self.speed = f"{int(data['wind']['speed'])}km/h"
            self.location = f"{self.city.capitalize()}, {self.country}"
            self.clothing_advice = get_clothing_advice(int(data['main']['temp']), data["weather"][0]["main"].lower())
            self.weather_condition = data["weather"][0]["main"].lower()
            self.error_message = ""
            
            # set the type of image based on the weather.
            weather_main = data["weather"][0]["main"].lower()
            self.image_src = WEATHER_IMAGE_MAP.get(weather_main, "/sunny.png")

            self.user_input = ""
            
        elif response.status_code != 200:
            self.error_message = "City not found. Please enter a valid city name."
            self.user_input = ""
        
        
        
    form_data: dict = {}
    
    def handle_submit(self, form_data:dict):
        self.form_data = form_data
            

# Clothing advice algorithm: Provides clothing advice based on the given temperature and weather condition.
def get_clothing_advice(temp, weather_condition):
    if temp > 30:
        return "Whoa, it's sizzling out there! Time for shorts and a tank top!"
    elif 20 < temp <= 30:
        if "rain" in weather_condition:
            return "Warm but wet, eh? Go for a tee and don't forget that umbrella!"
        return "It's T-shirt weather! Maybe grab some sunglasses too."
    elif 10 < temp <= 20:
        if "rain" in weather_condition:
            return "A bit chilly with a splash! A jacket and maybe an umbrella will serve you well."
        return "Feeling the breeze? A sweater or a light jacket should do the trick."
    else:
        if "snow" in weather_condition:
            return "Brrr! Snowball fight anyone? Bundle up with a thick coat, gloves, and a hat!"
        return "Freezing cold! Time to rock that winter coat and maybe a scarf and gloves!"