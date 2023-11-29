import reflex as rx
import pandas as pd
import requests
import os
import datetime
from dotenv import load_dotenv
from urllib.parse import urlencode
from typing import List, Dict
from sqlmodel import SQLModel, Field, create_engine

# CSS Stylesheet
# Defines styles for various components
WIDTH: list[str] = ["90%", "80%", "70%", "65%", "55%"]
css: dict = {
    "app": {"_dark": {"bg": "#1f2028"}},
    "header": {
        "width":"100%",
        "height":"60px",
        "box_shadow":"0px 8px 16px 0px rgba(0,0,0,0.25)",
        "padding": [
            "0 1rem",
            "0 1rem",
            "0 1rem",
            "0 4rem",
            "0 10rem",
        ],
        "_dark": {"bg":"#141518"},
        "_light": {"bg":"#ffffff"},
        "transition": "all 300ms ease",
        "justify-content": "center",
    },
    "input":{
        "width": WIDTH,
        "height": "70px",
        "text_align": "center",
        "font size": "32px",
        "transition": "all 300ms ease",
    },
    "errormessage":{
        "width": WIDTH,
        "height": "70px",
        "color": "#3e8be7",
        "text_align": "center",
        "font size": "32px",
        "transition": "all 300ms ease",
    },
    "single_stack":{
        "width": "100%",
        "align_items": "center",
        "justify_content": "center",
        "display": "flex",
        "padding_top": "4rem",
    },
    "multiple_stack":{
        "align_items": "center",
        "justify_content": "space-between",
        "display": "flex",
    },
    "content":{
        "width": WIDTH,
        "transition": "all 300ms ease",
        "border_radius": "10px",
        "justify_content": "center",
        "display": "flex",
        "overflow": "hidden",
        "box_shadow": "0px 10px 20px 0px rgba(0,0,0,0.5)",
    },
    "weather_image":{
        "color": "white",
        "spacing": "0",
        "width": "100%",
        "height": "inherit",
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
    },
    "weather_data_text":{
        "font_size": "10px",
        "font_weight": "bold",
        "opacity": "0.6",
        "_dark": {"color": "#000000"},
    },
}


# Header style: including the title, the breadcrumb navigation, and the dark/light mode toggle button.
# Pass the title as a parameter to the Header class.
class Header(rx.Hstack):
    def __init__(self, title_text="Home"):
        super().__init__(style=css.get("header"))

        self.title = rx.text(
            title_text,
            font_size="24px",
            background_image="linear-gradient(130deg, #3e8be7 40%, #87cefa 80%)",
            background_clip="text",
            font_weight="bold",
            style={"flex": 1, "margin-right": "20px"},
        )
              
        self.breadcrumbs = rx.breadcrumb(
            rx.breadcrumb_item(
                rx.breadcrumb_link("Check Weather", href="/")
            ),
            rx.breadcrumb_item(
                rx.breadcrumb_link("Manage Wardrobe", href="/wardrobe")
            ),
        )
        
        self.toggle = rx.color_mode_button(
            rx.color_mode_icon(),
            color_scheme="gray",
            _dark={"color": "white"},
            _light={"color": "black"},
            style={"margin-left": "40px"},
        )
        
        self.children = [self.title, self.breadcrumbs, self.toggle]
        

# Weather Data: retrieve data from the OpenWeatherMap API.
# Get the API key from the environment variables.
load_dotenv()
API_KEY: str = os.getenv("KEY")


# A dictionary mapping different weather conditions to their respective image sources.
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


# API request: construct the URL based on the given city name.
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


# Wardrobe data: database setup and model definition
DATABASE_URL = "sqlite:///reflex.db"
engine = create_engine(DATABASE_URL)

class Items(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    type: str
    description: str
    
SQLModel.metadata.create_all(engine)


# The state defines all the variables in an app that can change, as well as the functions that change them.
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
    max_temp: str = ""
    min_temp: str = ""
    sunrise_time: str = ""
    sunset_time: str = ""
    
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
        if self.content_bg != "#fafafa":
            self.content_bg = "#fafafa"
    
    def expand_content_height(self):
        if self.content_height != "300px":
            self.content_height = "300px"
            
    async def get_weather_data(self):
        city_name = self.cityname_input
        response = requests.get(get_weather_request(city_name))
        
        # If the city name is found, display the weather data.
        if response.status_code == 200:
            data = response.json()
            
            self.city = self.cityname_input
            self.country = data["sys"]["country"]
            self.temperature = f"{int(data['main']['temp'])}"
            self.humidity = f"{int(data['main']['humidity'])}"
            self.speed = f"{int(data['wind']['speed'])}"
            self.location = f"{self.city.capitalize()}, {self.country}"
            self.clothing_advice = get_clothing_advice(int(data['main']['temp']), data["weather"][0]["main"].lower())
            self.weather_condition = data["weather"][0]["main"].lower()
            self.weather_error_message = ""
            
            self.max_temp = f"{int(data['main']['temp_max'])}°C"
            self.min_temp = f"{int(data['main']['temp_min'])}°C"
            
            # Convert sunrise and sunset times to human-readable format
            sunrise_timestamp = int(data['sys']['sunrise'])
            sunset_timestamp = int(data['sys']['sunset'])
            
             # Assume the timestamp is in local time
            local_tz = datetime.timezone(datetime.timedelta(seconds=data['timezone']))
    
            self.sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp, tz=local_tz).strftime('%H:%M')
            self.sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp, tz=local_tz).strftime('%H:%M')
            
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
    all_items: List[Items] = []
    data: List[Dict] = []
    def __init__(self):
        super().__init__()
        self.all_items = []
        self.data = []
    
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
        self.data = [{"id": item.id, "name": item.name, "type": item.type, "description": item.description}
                     for item in items_list
                     ]
    
    # Delete the latest item from the database.
    def delete_latest_item(self):
        with rx.session() as session:
            latest_item = session.query(Items).order_by(Items.id.desc()).first()
            if latest_item:
                session.delete(latest_item)
                session.commit()
        self.fetch_data()
        
    # Delete the selected item from the database.
    delete_item_id: str = ""
    
    def delete_selected_item(self):
        with rx.session() as session:
            item_id = int(self.delete_item_id)
            item_to_delete = session.query(Items).filter(Items.id == item_id).first()
            if item_to_delete:
                session.delete(item_to_delete)
                session.commit()
        self.fetch_data()
        self.delete_item_id = ""
    
    def handle_delete_item_id_change(self, value):
        self.delete_item_id = value

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
    
# Instantiate the State class
state = State()

# Weather page: users can check the weather and receive clothing advice.
@rx.page(title='Weather Assistant')
def index() -> rx.Component :
 
    weather_header: rx.Hstack = Header("Weather Assistant")
    
    return rx.vstack(
        weather_header,
        
        # input area
        rx.vstack(
            rx.input(
                value=State.cityname_input,
                on_change=State.get_input_value,
                on_key_down=State.handle_key_press,
                placeholder="Enter a city name to get the weather",
                style=css.get("input"),
                ),
            rx.cond(
                State.weather_error_message, 
                rx.text(State.weather_error_message, style=css.get("errormessage")),
                None
            ),
            style=css.get("single_stack"),
        ), 
    
        # blank row
        rx.divider(height="2rem", border_color="transparent"),
        
        # weather data
        rx.hstack(
            # location and image
            rx.container(
                rx.vstack(
                    rx.image(
                        src=State.image_src,
                        html_height="100px",
                        html_width="100px",
                        ),
                        rx.heading(State.weather_condition.upper(), size="lg"),
                        rx.heading(State.location, size="md", opacity="0.8"),
                        style=css.get("weather_image"),
                    ),
                width=["35%"],
                height="inherit",
                bg="linear-gradient(220deg, #3e8be7 2.5%, #87cefa 97%)",  
                ),
            
            # weather details
            rx.container(
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.hstack(
                                rx.heading(State.temperature, size="xl"),
                                rx.heading("°C", size="md"),
                                      ),
                            rx.text(
                                "TEMPERATURE",
                                style=css.get("weather_data_text"),
                                ),
                                spacing="0",                       
                            ), 
                        rx.vstack(
                            rx.hstack(
                                rx.heading(State.humidity, size="xl"),
                                rx.heading("%", size="md"),
                                      ),
                            rx.text(
                                "HUMIDITY",
                                style=css.get("weather_data_text"),
                                ),
                                spacing="0",                    
                            ),
                        rx.vstack(
                            rx.hstack(
                                rx.heading(State.speed, size="xl"),
                                rx.heading("km/h", size="md"),
                                      ),
                            rx.text(
                                "WIND SPEED",
                                style=css.get("weather_data_text"),
                                ),
                                spacing="0",                     
                            ),
                        style=css.get("multiple_stack"),
                        width=["90%"],
                        padding_bottom="1.5rem",
                        ),

                    rx.hstack(
                        rx.vstack(
                            rx.heading(State.min_temp + " ~ " + State.max_temp, color="black", size="md"),
                            rx.text(
                                "LOW ~ HIGH",
                                style=css.get("weather_data_text"),
                                ),
                                spacing="0",                   
                            ),   
                        rx.vstack(
                            rx.heading(State.sunrise_time + " ~ " + State.sunset_time, color="black", size="md"),
                            rx.text(
                                "SUNRISE ~ SUNSET",
                                style=css.get("weather_data_text"),
                                ),
                                spacing="0",
                            ), 
                        style=css.get("multiple_stack"),
                        width=["65%"],
                        padding_top="1.5rem",
                        ),
                    width=["100%"],
                    height="inherit",
                    ),
                width=["65%"],
                ),
            height=State.content_height,
            bg=State.content_bg,
            style=css.get("content"),
            spacing="0",
        ),
        
        # blank row
        rx.divider(height="2rem", border_color="transparent"), 
        
        # clothing advice
        rx.text(State.clothing_advice, font_weight="bold", color="#3e8be7",),
    )


# Wardrobe page: users can manage items in their wardrobe.
@rx.page(title='My Wardrobe', route="/wardrobe")
def wardrobe_page() -> rx.Component:
        
    wardrobe_header: rx.Hstack = Header("My Wardrobe")

    # Use the state instance to call fetch_data
    state.fetch_data()
    # Convert state.data into a pandas dataframe
    df = pd.DataFrame(state.data)
    
    return rx.vstack(
        wardrobe_header,
        rx.box(height="2rem"),
        rx.card(
            rx.hstack(
                rx.form(            
                    rx.vstack(
                        rx.input(placeholder="name", id="name"),
                        rx.input(placeholder="type", id="type"),
                        rx.input(placeholder="description", id="description"),
                        rx.button("Add Item", type_="submit"),
                        #style=css.get("narrow_stack"),
                    ),
                    on_submit=State.handle_submit,
                ),
                rx.divider(height="5rem", border_color="gray", orientation="vertical"),
                rx.form(
                    rx.vstack(
                        rx.input(
                            placeholder="Enter Item ID to delete",
                            id="delete_item_id",
                            on_change=State.handle_delete_item_id_change
                        ),
                        rx.button(
                            "Delete Selected Item",
                            variant="solid",
                            on_click=State.delete_selected_item
                        ),
                        #style=css.get("narrow_stack"),
                    ),
                ),
                rx.divider(height="5rem", border_color="gray", orientation="vertical"),
                rx.form(
                    rx.stack(
                        rx.spacer(height="1rem"),
                        rx.text("The latest Item ID is" + " " + str(df["id"].iloc[-1]), color="gray",),
                        rx.spacer(height="1rem"),
                        rx.button(
                            "Delete Latest Item", 
                            variant="solid",
                            on_click=State.delete_latest_item,
                            ),
                        #style=css.get("narrow_stack"),
                    ),
                ),
                width="95%",
                justify_content="space-between",
                #align_items="flex-end",
            ),
            
            footer=rx.text(
                "To view the latest updates in your wardrobe, please restart the application after adding or deleting items. ", 
                size="sm",
                color="#3e8be7",
            ),
            width="95%",
        ),
        
        # blank row
        rx.divider(height="2rem", border_color="transparent"), 
        
        rx.hstack(
            rx.data_table(
                data=df,
                pagination=True,
                search=True,
                sort=True
            ),
            width="95%",
        ),
    )


# Initialize and configure the application
app = rx.App(style=css.get("app"))              # Initialize the main app with the defined styles.
app.add_page(index)                             # Add the main page to the app.
app.add_page(wardrobe_page, route="/wardrobe")  # Add the wardrobe page to the app.
app.compile()                                   # Compile the app