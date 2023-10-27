import reflex as rx
from urllib.parse import urlencode
from weather_assistant.state import State
from weather_assistant.style import css, WIDTH, Header
import pandas as pd


# weather page: users can check the weather and receive clothing advice.
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
                style=css.get("input"),
                placeholder="Enter a city name to get the weather",
                ),
            rx.cond(
                State.weather_error_message, 
                rx.text(State.weather_error_message, color="#3e8be7", style=css.get("input")),
                None
            ),
            style=css.get("stack"),
        ), 
    
        # blank row
        rx.divider(height="2em", border_color="transparent"),
        
        # weather data
        rx.hstack(
            # location and image
            rx.container(
                rx.vstack(
                    rx.image(
                        src=State.image_src,
                        html_height="100px",
                        html_width="100px",
                        #filter="brightness(0) invert(1)",
                        ),
                        rx.heading(State.location, size="md"),
                        rx.text(State.weather_condition, font_weight="bold", opacity="0.6"),
                        color="white",
                        spacing="0",
                        width="100%",
                        height="inherit",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                    ),
                width=["30%", "30%", "30%", "35%", "35%"],
                height="inherit",
                bg="linear-gradient(220deg, #3e8be7 2.5%, #87cefa 97%)",  
                ),
            
            # weather details
            rx.container(
                rx.hstack(
                    rx.vstack(
                        rx.heading(State.temperature, size="2xl"),
                        rx.text(
                            "TEMPERATURE",
                            font_size="10px",
                            font_weight="bold",
                            opacity="0.6",
                            ),
                            spacing="0",                       
                        ), 
                    rx.vstack(
                        rx.heading(State.speed, size="2xl"),
                        rx.text(
                            "WIND SPEED",
                            font_size="10px",
                            font_weight="bold",
                            opacity="0.6",
                            ),
                            spacing="0",                       
                        ),
                    rx.vstack(
                        rx.heading(State.humidity, size="2xl"),
                        rx.text(
                            "HUMIDITY",
                            font_size="10px",
                            font_weight="bold",
                            opacity="0.6",
                            ),
                            spacing="0",                       
                        ),          
                    width="100%",
                    height="inherit",
                    display="flex",
                    align_items="center",
                    justify_content="space-between",
                    color="black",
                    ),
                width=["70%", "70%", "70%", "65%", "65%"],
                height="inherit",
                ),
            height=State.content_height,
            bg=State.content_bg,
            style=css.get("content"),
            spacing="0",
        ),
        
        # blank row
        rx.divider(height="2em", border_color="transparent"), 
        
        # clothing advice
        rx.text(State.clothing_advice, font_weight="bold", style=css.get("input")),
        
        style=css.get("main"),  
    )



# wardrobe page: users can manage items in their wardrobe.
@rx.page(title='Wardrobe Manager', route="/wardrobe")
def wardrobe_page() -> rx.Component:
        
    wardrobe_header: rx.Hstack = Header("My Wardrobe")
    
    # Instantiate the State class
    state = State()
    # Use the state instance to call fetch_data
    state.fetch_data()
    # Convert state.data into a pandas dataframe
    df = pd.DataFrame(state.data)
    
    return rx.vstack(
        wardrobe_header,
        # input area        
        rx.form(            
            rx.vstack(
                rx.input(placeholder="name", id="name"),
                rx.input(placeholder="type", id="type"),
                rx.input(placeholder="description", id="description"),
                rx.button("Submit", type_="submit"),
                style=css.get("stack"),
            ),
            on_submit=State.handle_submit,
        ),
        rx.data_table(
            data=df,
            pagination=True,
            search=True,
            sort=True
        ),
    )



app = rx.App(style=css.get("app"))              # Initialize the main app with the defined styles.
app.add_page(index)                             # Add the main page to the app.
app.add_page(wardrobe_page, route="/wardrobe")  # Add the wardrobe page to the app.
app.compile()                                   # Compile the app