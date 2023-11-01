import reflex as rx
from sqlmodel import SQLModel, Field, create_engine, Session


DATABASE_URL = "sqlite:///reflex.db"
engine = create_engine(DATABASE_URL)

class Items(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    type: str
    description: str
    
SQLModel.metadata.create_all(engine)    