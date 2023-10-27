import reflex as rx                 # Reflex is a Python library for creating web applications.
from urllib.parse import urlencode  # Encode URL parameters.
from weather_assistant.state import State, AddItems, QueryWardrobe
from weather_assistant.style import css, WIDTH, Header


# main page: the user can input a city name to get the weather and receive clothing advice.
@rx.page(title='Weather Assistant')
def index() -> rx.Component :

    weather_header: rx.Hstack = Header("Weather Assistant")
    
    return rx.vstack(
        weather_header,
        
        # input area
        rx.vstack(
            rx.input(
                value=State.user_input,
                on_change=State.get_input_value,
                on_key_down=State.handle_key_press,
                style=css.get("input"),
                placeholder="Enter a city name to get the weather",
                ),
            rx.cond(
                State.error_message, 
                rx.text(State.error_message, color="#3e8be7", style=css.get("input")),
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
                        rx.heading(State.temp, size="2xl"),
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


@rx.page(title='Weather Assistant', route="/wardrobe")
def wardrobe_page() -> rx.Component:
    
    wardrobe_header: rx.Hstack = Header("My Wardrobe")
    
    return rx.vstack(
        wardrobe_header,
        
        
    )



app = rx.App(style=css.get("app"))         # Initialize the main app with the defined styles.
app.add_page(index)                        # Add the main page to the app.
app.add_page(wardrobe_page, route="/wardrobe")  # Add the wardrobe page to the app.
app.compile()                              # Compile the app