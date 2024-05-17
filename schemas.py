from pydantic import BaseModel

class Item(BaseModel):
    name: str
    type: str
    sprite: str
    catchrate: int
