from fastapi import FastAPI
import mysql.connector
import schemas

app = FastAPI()

host_name = "database-1.cpxnwinne8ao.us-east-1.rds.amazonaws.com"
port_number = "3306"
user_name = "admin"
password_db = "CC-utec_2024-s3"
database_name = "pokemons"  

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
    cursor.execute(f"SELECT * FROM pokemons WHERE pokemon_id = {id}")
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
    hp = item.hp
    nivel = item.level
    ataque = item.attack
    defensa = item.defense
    velocidad = item.speed
    cursor = mydb.cursor()
    sql = "INSERT INTO pokemons (pokemon_nombre, tipo, hp, nivel, ataque, defensa, velocidad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (nombre, tipo, hp, nivel, ataque, defensa, velocidad)
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
    hp = item.hp
    nivel = item.level
    ataque = item.attack
    defensa = item.defense
    velocidad = item.speed
    cursor = mydb.cursor()
    sql = "UPDATE pokemons SET pokemon_nombre=%s, tipo=%s, hp=%s, nivel=%s, ataque=%s, defensa=%s, velocidad=%s WHERE pokemon_id=%s"
    val = (nombre, tipo, hp, nivel, ataque, defensa, velocidad, id)
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
    cursor.execute(f"DELETE FROM pokemons WHERE pokemon_id = {id}")
    mydb.commit()
    mydb.close()
    return {"message": "Pokemon deleted successfully"}
