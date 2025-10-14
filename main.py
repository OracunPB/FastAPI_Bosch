from fastapi import FastAPI

app = FastAPI()

users = [{"id":1, "nom":"Pau"}]

@app.post("/api/users", response_model=dict)
async def insert_user():
    return {"user":"Pau"}

@app.get("/api/users/{id}", response_model=dict)
async def get_user():
    return{"user":{id}}

@app.get("/api/users", response_model=dict)
async def get_users():
    return{""}