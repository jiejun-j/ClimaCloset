import reflex as rx


class Items(rx.Model, table=True):
    name: str
    type: str
    color: str
    preference_temperature: str
    image: str