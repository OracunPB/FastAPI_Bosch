from fastapi import FastAPI

app = FastAPI()

users = [
    {"id":1, "nom":"Pau", "edat": "30"},
    {"id":2, "nom":"Mireia", "edat": "29"},
    {"id":3, "nom":"Sergi", "edat": "30"}
]

#1 Crear - Afegir a la list
@app.post("/api/users")
async def insert_user(user: dict):
    users.append(user)
    return {"user":users}

#2 Llegir - Consultar un usuari / objecte de la llista
@app.get("/api/users/{id}")
async def get_user(id: int):
    return{"user":users[id - 1]}

#3 Llegir - Consultar tots els usuaris
@app.get("/api/users")
async def get_users():
    return{"users":users}

#4 Actualitzar - Actualització completa
@app.put("/api/users/{id}")
async def update_user(id:int, canvis: dict):
    users[id-1].update(canvis)
    return {"users": users}

#6 Eliminar - Esborrar usuari
@app.delete("/api/users/{id}")
async def delete_user(id: int):
    users.pop(id-1)
    return {"users": users}
