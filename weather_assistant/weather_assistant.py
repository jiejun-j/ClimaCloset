import reflex as rx
import pandas as pd
import requests
import datetime
from sqlmodel import SQLModel, Field, create_engine, select

# CSS Stylesheet
css: dict = {
    "header_container": {
        "width":"100%",
        "height":"60px",
        "box_shadow":"0px 8px 16px 0px rgba(0,0,0,0.1)",
        "padding": "0 10rem", 
        "justify-content": "space-between",
    },
    "header_title": {
        "font_size":"24px",
        "font_weight":"bold",
        "color":"#3e8be7",
    },
    "input":{
        "width": "55%",
        "height": "70px",
        "text_align": "center",
        "font size": "32px",
    },
    "errormessage":{
        "width": "55%",
        "height": "70px",
        "text_align": "center",
        "font size": "32px",
        "color": "#3e8be7",
    },
    "single_stack":{
        "width": "100%",
        "align_items": "center",
        "justify_content": "center",
        "padding_top": "4rem",
    },
    "multiple_stack":{
        "align_items": "center",
        "justify_content": "space-between",
    },
    "content":{
        "width": "55%",
        "border_radius": "10px",
        "justify_content": "center",
        "overflow": "hidden",
        "box_shadow": "0px 10px 20px 0px rgba(0,0,0,0.15)",
    },
    "weather_image":{
        "color": "white",
        "width": "100%",
        "height": "inherit",
        "align_items": "center",
        "justify_content": "center",
    },
    "weather_data_attributes":{
        "font_size": "12px",
        "font_weight": "bold",
        "opacity": "0.6",
    },
    "weather_data_big_numbers":{
        "font_size": "45px",
        "font_weight": "bold",
    },
    "weather_data_small_numbers":{
        "font_size": "24px",
        "font_weight": "bold",
    },
    "weather_data_measurement":{
        "font_size": "24px",
        "font_weight": "bold",
        "height": "18px",
    },
}


# Weather API: get the weather data for the given city.
def get_weather_request(city: str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    full_url = f"{base_url}?q={city}&appid=7c9495e301fb54d62adb32527d93cc87&units=metric"
    return full_url

# Weather images: map the weather condition to the corresponding image.
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


# Wardorbe Database: create a database to store the wardrobe items.
DATABASE_URL = "sqlite:///reflex.db"
engine = create_engine(DATABASE_URL)

# Items table: define the table schema.
class Items(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str
    name: str
    suitable_temperature: str
    is_waterproof: str

# Create the table in the database.
SQLModel.metadata.create_all(engine)

# Clothing types: the types of clothing that can be added to the wardrobe.
clothing_types: list[str] = ["Top", "Bottom", "Dress", "Shoes", "Accessory"]

# Temperature types:
temperature_types: list[str] = ["Hot", "Warm", "Cool", "Cold", "Freeze"]

def get_temperature_type(temperature: int):
    if temperature > 30:
        return "Hot"
    elif 20 < temperature <= 30:
        return "Warm"
    elif 10 < temperature <= 20:
        return "Cool"
    elif 0 < temperature <= 10:
        return "Cold"
    else:
        return "Freeze"

# Default clothing advice: Provides clothing advice based on the given temperature and weather condition.
def get_default_clothing_advice(temperature, weather_condition):
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


# The State class defines all the variables that can change, as well as the event handlers that change them.
class State(rx.State):
    # Weather attributes
    weather_condition: str = ""
    image_src: str = ""
    location: str = ""
    city: str = ""
    country: str = ""
    temperature: str = ""
    speed: str = ""
    humidity: str = ""
    max_temp: str = ""
    min_temp: str = ""
    sunrise_time: str = ""
    sunset_time: str = ""
    
    # Input attributes
    cityname_input: str = ""
    weather_error_message: str = ""
    
    # Get the city name entered by the user.
    def get_input_value(self, cityname_input):
        self.cityname_input = cityname_input
    
    # When the user presses the Enter key, update the content style and get the weather data.
    def handle_key_press(self, key):
        if key == "Enter" and self.cityname_input != "":
            self.get_weather_data()
    
    # Display the content area.
    content_height: str = "0px"
    content_bg: str = ""
    def update_content_style(self):
        if self.content_height != "300px":
            self.content_height = "300px"
        if self.content_bg != "#fafafa":
            self.content_bg = "#fafafa"
    
    # Get the weather data for the given city.
    def get_weather_data(self):
        city_name = self.cityname_input
        
        # get the weather data from the API
        response = requests.get(get_weather_request(city_name))
        
        # If the city name is found, display the weather data.
        if response.status_code == 200:
            data = response.json()
            
            # display the content area
            self.update_content_style()
            
            # set the image source based on the weather condition
            weather_main = data["weather"][0]["main"].lower()
            self.image_src = WEATHER_IMAGE_MAP.get(weather_main, "/sunny.png")
            
            # set the weather data
            self.city = self.cityname_input
            self.country = data["sys"]["country"]
            self.temperature = f"{int(data['main']['temp'])}"
            self.humidity = f"{int(data['main']['humidity'])}"
            self.speed = f"{int(data['wind']['speed'])}"
            self.location = f"{self.city.capitalize()}, {self.country}"
            self.weather_condition = data["weather"][0]["main"].lower()
            self.weather_error_message = ""
            
            self.max_temp = f"{int(data['main']['temp_max'])}°C"
            self.min_temp = f"{int(data['main']['temp_min'])}°C"
            
            sunrise_timestamp = int(data['sys']['sunrise'])
            sunset_timestamp = int(data['sys']['sunset'])
            
            # Assume the timestamp is in local time
            local_tz = datetime.timezone(datetime.timedelta(seconds=data['timezone']))

            # Convert the timestamp to a datetime object and format it
            self.sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp, tz=local_tz).strftime('%H:%M')
            self.sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp, tz=local_tz).strftime('%H:%M')
            
            # Clear the input field
            self.cityname_input = ""
            
            # Set the clothing advice
            self.set_clothing_advice()
        
        # If the city name is not found, display an error message.
        elif response.status_code != 200:
            self.weather_error_message = "City not found. Please enter a valid city name."
            self.cityname_input = ""

    # Clothing advice: Provides clothing advice based on the weather condition and wardrobe items.
    clothing_advice: str = ""
    def set_clothing_advice(self):
        temp = int(self.temperature)
        condition = self.weather_condition.lower()
        temperature_situation = get_temperature_type(temp)
        is_wet_condition = "True" if "rain" in condition or "snow" in condition else "False"
        
        recommendations = self.fetch_recommendations(temperature_situation, is_wet_condition)
        
        if len(recommendations) > 0:
            self.clothing_advice = "You can wear "
            self.clothing_advice += ', '.join([recommendation["name"] for recommendation in recommendations])
            self.clothing_advice += " today."
        else:
            self.clothing_advice = "We didn't find any suitable clothing in your wardrobe. Here is a general advice: \n"
            self.clothing_advice += get_default_clothing_advice(temp, condition)
    
    
    # Wardrobe attributes
    all_items: list[Items] = [] 
    data: list[dict] = [] 
    def __init__(self):
        super().__init__()
        self.all_items = []
        self.data = []
    
    # Set the selected type and reselected type
    selected_type: str = ""
    selected_is_waterproof: str = ""
    selected_suitable_temperature: str = ""
    reselected_type: str = ""
    reselected_is_waterproof: str = ""
    reselected_suitable_temperature: str = ""
    
    def set_selected_type(self, value):
        self.selected_type = value
        
    def set_reselected_type(self, value):
        self.reselected_type = value
        
    def set_selected_is_waterproof(self, value):
        self.selected_is_waterproof = value
        
    def set_reselected_is_waterproof(self, value):
        self.reselected_is_waterproof = value
        
    def set_selected_suitable_temperature(self, value):
        self.selected_suitable_temperature = value
        
    def set_reselected_suitable_temperature(self, value):
        self.reselected_suitable_temperature = value
        
    # Fetch the recommendations from the database.
    def fetch_recommendations(self, suitable_temperature, is_waterproof):
        with rx.session() as session:
            statement = select(Items) \
                .where(Items.suitable_temperature == suitable_temperature) \
                .where(Items.is_waterproof == is_waterproof)
            recommendations = session.exec(statement).all()
            return [{"id": item.id, 
                      "name": item.name, 
                      "type": item.type, 
                      "suitable_temperature": item.suitable_temperature,
                      "is_waterproof": item.is_waterproof,
                      }
                     for item in recommendations]
    
    # Fetch the data from the database.
    def fetch_data(self):
        with rx.session() as session:
            statement = select(Items)
            items_list = session.exec(statement).all()
            self.data = [{"id": item.id, 
                          "name": item.name, 
                          "type": item.type, 
                          "suitable_temperature": item.suitable_temperature,
                          "is_waterproof": item.is_waterproof,
                          }
                         for item in items_list]
    
    # Add a new item to the database.
    def handle_add_submit(self, form_data:dict):
        with rx.session() as session:
            data = Items(
                type=self.selected_type,
                name=form_data.get("name"),
                suitable_temperature=self.selected_suitable_temperature,
                is_waterproof=self.selected_is_waterproof,
            )
            session.add(data)
            session.commit()
        app = rx.App()
        app.compile()
    
    # Edit an existing item in the database.
    def handle_edit_submit(self, form_data: dict):
        item_id = form_data.get("edit_id")
        new_type = self.reselected_type
        new_name = form_data.get("edit_name")
        new_suitable_temperature = self.reselected_suitable_temperature
        new_is_waterproof = self.reselected_is_waterproof
        with rx.session() as session:
            # search for the item to edit
            item_to_edit = session.query(Items).filter(Items.id == int(item_id)).first()
            if item_to_edit:
                # update the item
                item_to_edit.type = new_type
                item_to_edit.name = new_name
                item_to_edit.suitable_temperature = new_suitable_temperature
                item_to_edit.is_waterproof = new_is_waterproof
                session.commit()
        app = rx.App()
        app.compile()

    # Delete the latest item from the database.
    def delete_latest_item(self):
        with rx.session() as session:
            statement = select(Items).order_by(Items.id.desc())
            latest_item = session.exec(statement).first()
            if latest_item:
                session.delete(latest_item)
                session.commit()
        app = rx.App()
        app.compile()
        
    # Delete the selected item from the database.
    delete_item_id: str = ""
    def delete_selected_item(self):
        with rx.session() as session:
            item_id = int(self.delete_item_id)
            item_to_delete = session.query(Items).filter(Items.id == item_id).first()
            if item_to_delete:
                session.delete(item_to_delete)
                session.commit()
        self.delete_item_id = ""
        app = rx.App()
        app.compile()
    
    def handle_delete_item_id_change(self, value):
        self.delete_item_id = value
        

# Instantiate the State class
state = State()


# Header style: including the title and the breadcrumb navigation
# Pass the title as a parameter to the Header class.
class Header(rx.Hstack):
    def __init__(self, title_text=""): # default title is empty
        super().__init__(style=css.get("header_container")) 

        self.title = rx.text(
            title_text,
            style=css.get("header_title"),
        )
              
        self.breadcrumbs = rx.breadcrumb(
            rx.breadcrumb_item(
                rx.breadcrumb_link("Check Weather", href="/")
            ),
            rx.breadcrumb_item(
                rx.breadcrumb_link("Manage Wardrobe", href="/wardrobe")
            ),
        )
        
        self.children = [self.title, self.breadcrumbs]


# Weather page: users can check the weather and receive clothing advice.
@rx.page(title='Weather Assistant')
def index() -> rx.Component :
    
    # Create the header
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
    
        # add a space between the input area and the weather data
        rx.box(height="3rem"),
        
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
                    # temperature, humidity, wind speed
                    rx.hstack(
                        rx.vstack(
                            rx.hstack(
                                rx.heading(State.temperature, style=css.get("weather_data_big_numbers")),
                                rx.heading("°C", style=css.get("weather_data_measurement"),),
                                    vertical_align="bottom",
                                      ),
                            rx.text("TEMPERATURE", style=css.get("weather_data_attributes"),),
                                spacing="0",
                            ), 
                        rx.vstack(
                            rx.hstack(
                                rx.heading(State.humidity, style=css.get("weather_data_big_numbers")),
                                rx.heading("%", style=css.get("weather_data_measurement"),),
                                      ),
                            rx.text("HUMIDITY", style=css.get("weather_data_attributes"),),
                                spacing="0",
                            ),
                        rx.vstack(
                            rx.hstack(
                                rx.heading(State.speed, style=css.get("weather_data_big_numbers")),
                                rx.heading("km/h", style=css.get("weather_data_measurement"),),
                                      ),
                            rx.text("WIND SPEED", style=css.get("weather_data_attributes"),),
                                spacing="0",
                            ),
                        style=css.get("multiple_stack"),
                        width=["90%"],
                        padding_bottom="1.5rem",
                        ),
                    # min temp, max temp, sunrise time, sunset time
                    rx.hstack(
                        rx.vstack(
                            rx.heading(
                                State.min_temp + " ~ " + State.max_temp, 
                                style=css.get("weather_data_small_numbers"),
                                ),
                            rx.text("LOW ~ HIGH", style=css.get("weather_data_attributes"),),
                                spacing="0",                   
                            ),   
                        rx.vstack(
                            rx.heading(
                                State.sunrise_time + " ~ " + State.sunset_time, 
                                style=css.get("weather_data_small_numbers"),
                                ),
                            rx.text("SUNRISE ~ SUNSET", style=css.get("weather_data_attributes"),),
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
        
        # clothing advice
        rx.text(State.clothing_advice, font_weight="bold", color="#3e8be7", padding_top="50px"),
    )


# Wardrobe page: users can manage items in their wardrobe.
@rx.page(title='My Wardrobe', route="/wardrobe")
def wardrobe_page() -> rx.Component:
    
    # Create the header
    wardrobe_header: rx.Hstack = Header("My Wardrobe")

    # Use the state instance to call fetch_data
    state.fetch_data()
    
    # Convert state.data into a pandas dataframe
    df = pd.DataFrame(state.data)
    
    # Check if the dataframe is empty, and if it is, display a message.
    if "id" in df.columns and not df.empty:
        latest_item_id_text = "The latest Item ID is " + str(df["id"].iloc[-1])
    else:
        latest_item_id_text = "There are no items"
    
    return rx.vstack(
        wardrobe_header,
        rx.box(height="2rem"),
        
        # Manage wardrobe area
        rx.card(
            rx.hstack(
                rx.box(width="1rem"),
                
                # Add item
                rx.form(           
                    rx.vstack(
                        rx.select(
                            clothing_types,
                            placeholder="Select Type",
                            on_change=State.set_selected_type,
                            value=State.selected_type,
                        ),
                        rx.input(placeholder="Name (e.g., Jeans)", id="name"),
                        rx.select(
                            temperature_types,
                            placeholder="Select suitable temperature",
                            on_change=State.set_selected_suitable_temperature,
                            value=State.selected_suitable_temperature,
                        ),
                        rx.select(
                            ["True", "False"],
                            placeholder="Is your clothes waterproof?",
                            on_change=State.set_selected_is_waterproof,
                            value=State.selected_is_waterproof,
                        ),
                        rx.button("Add Item", type_="submit"),
                        style=css.get("multiple_stack"),
                    ),
                    on_submit=State.handle_add_submit,
                ),
                rx.divider(height="10rem", orientation="vertical"),
                
                # Edit item
                rx.form(
                    rx.vstack(
                        rx.input(placeholder="ID", id="edit_id"),
                        rx.select(
                            clothing_types,
                            placeholder="New Select Type",
                            on_change=State.set_reselected_type,
	                        value=State.reselected_type,
                        ),
                        rx.input(placeholder="New Name", id="edit_name"),
                        rx.select(
                            temperature_types,
                            placeholder="Select suitable temperature",
                            on_change=State.set_reselected_suitable_temperature,
                            value=State.reselected_suitable_temperature,
                        ),
                        rx.select(
                            ["True", "False"],
                            placeholder="Is your clothes waterproof?",
                            on_change=State.set_reselected_is_waterproof,
                            value=State.reselected_is_waterproof,
                        ),
                        rx.button("Edit Item", type_="submit"),
                    ),
                    on_submit=State.handle_edit_submit,
                ),
                rx.divider(height="10rem", orientation="vertical"),
                
                # Delete selected item
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
                rx.divider(height="10rem", orientation="vertical"),
                
                # Delete latest item
                rx.form(
                    rx.stack(
                        rx.spacer(height="1rem"),
                        rx.text(latest_item_id_text, color="gray",),
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
            ),
            width="80%",
            padding="2rem",
        ),
        
        # Display the wardrobe items in a data table
        rx.hstack(
            rx.data_table(
                data=df,
                pagination=True,
                search=True,
                sort=True
            ),
            width="85%",
            padding="2rem",
        ),
    )


# Initialize and configure the application
app = rx.App()
app.add_page(index)
app.add_page(wardrobe_page, route="/wardrobe")
app.compile()