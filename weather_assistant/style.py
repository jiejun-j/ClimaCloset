import reflex as rx

# style sheet
WIDTH: list[str] = ["90%", "80%", "70%", "65%", "55%"]

css: dict = {
    "app": {"_dark": {"bg": "#1f2028"}},
    "main": {"width": "100%", "height": "100vh"},
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
    "stack":{
        "width": "100%",
        "align_items": "center",
        "justify_content": "center",
        "display": "flex",
        "padding_top": "4rem",
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
}


# header style: including the title and the dark/light mode toggle button.
# pass the title as a parameter to the Header class.
class Header(rx.Hstack):
    def __init__(self, title_text="Home"):
        super().__init__(style=css.get("header"))
        self.toggle = rx.color_mode_button(
            rx.color_mode_icon(),
            color_scheme="None",
            _dark={"color": "white"},
            _light={"color": "black"},
            style={"margin-left": "40px"},
        )

        self.title = rx.text(
            title_text,
            font_size="24px",
            background_image="linear-gradient(130deg, #3e8be7 40%, #87cefa 80%)",
            background_clip="text",
            font_weight="bold",
            style={"flex": 1, "margin-right": "20px"},
        )
        
        self.link_weather = rx.link(
            "Search Weather",
            href="/",
            style={"margin-right": "40px", "font-size": "16px"},
        )
        
        self.link_wardrobe = rx.link(
            "Manage Wardrobe",
            href="/wardrobe",
            style={"margin-right": "40px", "font-size": "16px"},
        )
        
        self.separator = rx.divider(
            orientation="vertical",
            height="14px",
            border_color="rgba(0,0,0,0.5)",
            style={"margin-right": "40px"},
        )

        self.children = [self.title, self.link_weather, self.separator, self.link_wardrobe, self.toggle]