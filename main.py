from fastapi import FastAPI
import mysql.connector
import schemas
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Salt to your taste
ALLOWED_ORIGINS = '*'    # or 'foo.com', etc.

# handle CORS preflight requests
@app.options('/{rest_of_path:path}')
async def preflight_handler(request: Request, rest_of_path: str) -> Response:
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

# set CORS headers
@app.middleware("http")
async def add_CORS_header(request: Request, call_next):
    response = await call_next(request)
    response.headers['Access-Control-Allow-Origin'] = ALLOWED_ORIGINS
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response

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
    result = cursor.fetchall()
    mydb.close()
    return {"pokemons": result}

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
    return {"pokemon": result}

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
