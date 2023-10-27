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
    temperature: str = ""
    speed: str = ""
    humidity: str = ""
    weather_condition: str = ""
    image_src: str = ""
    
    # Page content attributes
    cityname_input: str = ""
    clothing_advice: str = ""
    weather_error_message: str = ""
    
    # Styling attributes
    content_height: str = "0px"
    content_bg: str = ""
    
    def get_input_value(self, cityname_input):
        self.cityname_input = cityname_input
    
    async def handle_key_press(self, key):
        if key == "Enter" and self.cityname_input != "":
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
        response = requests.get(get_weather_request(self.cityname_input))
        await asyncio.sleep(0.05)
        
        # If the city name is found, display the weather data.
        if response.status_code == 200:
            data = response.json()
            
            self.city = self.cityname_input
            self.country = data["sys"]["country"]
            self.temperature = f"{int(data['main']['temperature'])}°C"
            self.humidity = f"{int(data['main']['humidity'])}%"
            self.speed = f"{int(data['wind']['speed'])}km/h"
            self.location = f"{self.city.capitalize()}, {self.country}"
            self.clothing_advice = get_clothing_advice(int(data['main']['temperature']), data["weather"][0]["main"].lower())
            self.weather_condition = data["weather"][0]["main"].lower()
            self.weather_error_message = ""
            
            # set the type of image based on the weather.
            weather_main = data["weather"][0]["main"].lower()
            self.image_src = WEATHER_IMAGE_MAP.get(weather_main, "/sunny.png")
            self.cityname_input = ""
        
        # If the city name is not found, display an error message.
        elif response.status_code != 200:
            self.weather_error_message = "City not found. Please enter a valid city name."
            self.cityname_input = ""
        
    
    # Wardrobe attributes
    # Create a session and query the table to add a new record to the database.
    all_items: list[Items] = []
    data: list[dict] = []
    
    def handle_submit(self, form_data:dict):
        with rx.session() as session:
            data = Items(
                name=form_data.get("name"),
                type=form_data.get("type"),
                description=form_data.get("description"),
            )
            session.add(data)
            session.commit()
        self.fetch_data()

    # Fetch the data from the database.
    def fetch_data(self):
        with rx.session() as session:
            items_list = session.query(Items).all()
        self.data = [{"name": item.name, "type": item.type, "description": item.description}
                     for item in items_list
                     ]

    # Delete the selected item from the database.
    def delete_item(self, name):
        with rx.session() as session:
            session.query(Items).filter_by(name=name).delete()
            session.commit()
        self.fetch_data()
    

# Clothing advice algorithm: Provides clothing advice based on the given temperature and weather condition.
def get_clothing_advice(temperature, weather_condition):
    if temperature > 30:
        return "Whoa, it's sizzling out there! Time for shorts and a tank top!"
    elif 20 < temperature <= 30:
        if "rain" in weather_condition:
            return "Warm but wet, eh? Go for a tee and don't forget that umbrella!"
        return "It's T-shirt weather! Maybe grab some sunglasses too."
    elif 10 < temperature <= 20:
        if "rain" in weather_condition:
            return "A bit chilly with a splash! A jacket and maybe an umbrella will serve you well."
        return "Feeling the breeze? A sweater or a light jacket should do the trick."
    else:
        if "snow" in weather_condition:
            return "Brrr! Snowball fight anyone? Bundle up with a thick coat, gloves, and a hat!"
        return "Freezing cold! Time to rock that winter coat and maybe a scarf and gloves!"