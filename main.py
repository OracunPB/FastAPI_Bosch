from fastapi import FastAPI

app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine()

#1 Crear - Afegir a la list
@app.post("/api/products")
async def insert_product(product: dict):
    products.append(product)
    return {"product":products}

#2 Llegir - Consultar un producte de la llista
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

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/user", response_model=dict, tags=["CREATE"])
def addUser(user: UserRequest, db:Session = Depends(get_db)):
    insert_user = User.model_validate(user)
    db.add(insert_user)
    db.commit()
    return {"msg":"Afegit usuari correctament"}


@app.get("/user/{id}", response_model=UserResponse, tags=["READ by ID"])
def getUser(id: int, db:Session = Depends(get_db)):
    stmt = select(User).where(User.id == id)
    result = db.exec(stmt).first()
    print(result) #pa ver lo que se printa
    return UserResponse.model_validate(result)

