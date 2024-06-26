from fastapi import FastAPI
import mysql.connector
import schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
class Pokemon:
    def __init__(self, id, nombre, tipo, sprite, catchrate):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.sprite = sprite
        self.catchrate = catchrate

# Function to build Pokemon objects
def build_pokemon_object(data):
    if data:
        id, nombre, tipo, sprite, catchrate = data
        return Pokemon(id=id, nombre=nombre, tipo=tipo, sprite=sprite, catchrate=catchrate)
    return None

ALLOWED_ORIGINS = '*'    # or 'foo.com', etc.


host_name = "database-1.cpxnwinne8ao.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin"
password_db = "CC-utec_2024-s3"
database_name = "pokemons"  

@app.get("")
def get_hola_mundo():
    return {"message": "Hola Mundo"}

# Get all pokemons
@app.get("/pokemons")
def get_pokemons():
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM pokemons")
    results = cursor.fetchall()
    mydb.close()
    
    pokemons = [build_pokemon_object(data) for data in results]
    return {"pokemons": pokemons}

# Get a pokemon by ID
@app.get("/pokemons/{id}")
def get_pokemon(id: int):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM pokemons WHERE id = {id}")
    result = cursor.fetchone()
    mydb.close()
    
    pokemon = build_pokemon_object(result)
    return {"pokemon": pokemon}

# Add a new pokemon
@app.post("/pokemons")
def add_pokemon(item: schemas.Item):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    nombre = item.name
    tipo = item.type
    sprite = item.sprite
    catchrate = item.catchrate
    cursor = mydb.cursor()
    sql = "INSERT INTO pokemons (nombre, tipo, sprite, catchrate) VALUES (%s, %s, %s, %s)"
    val = (nombre, tipo, sprite, catchrate)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Pokemon added successfully"}

# Modify a pokemon
@app.put("/pokemons/{id}")
def update_pokemon(id: int, item: schemas.Item):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    nombre = item.name
    tipo = item.type
    sprite = item.sprite
    catchrate = item.catchrate
    cursor = mydb.cursor()
    sql = "UPDATE pokemons SET nombre=%s, tipo=%s, sprite=%s, catchrate=%s WHERE id=%s"
    val = (nombre, tipo, sprite, catchrate, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Pokemon modified successfully"}

# Delete a pokemon by ID
@app.delete("/pokemons/{id}")
def delete_pokemon(id: int):
    mydb = mysql.connector.connect(
        host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
    )
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM pokemons WHERE id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Pokemon deleted successfully"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

