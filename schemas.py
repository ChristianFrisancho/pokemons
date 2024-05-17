from pydantic import BaseModel

class Item(BaseModel):
    name: str
    type: str
    hp: int
    level: int
    attack: int
    defense: int
    speed: int
