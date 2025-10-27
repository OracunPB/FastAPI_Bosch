from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


# products = []
#
# #1 Ceate - Afegir un nou registre a la taula
# @app.post("/api/products")
# async def insert_product(product: dict):
#     products.append(product)
#     return {"S'ha introduït correctament el producte"}
#
# #2 Read - Consultar totes les dades d’un registre a la taula.
# @app.get("/api/products/{id}")
# async def get_product(id: int):
#     return{"product":products[id - 1]}
#
# #3 Read - Consultar totes les dades de tots els registres de la taula.
# @app.get("/api/products")
# async def get_products():
#     return{"product":products}
# #Ha de conseguir mostrar ProductRequest
#
# #4 Read - Consultar les dades filtrant per un camp
# # @app.put("/api/products/{campo}")
# # async def get_product_spec(id:int):
# #    return {"product": products[campo]}
#
# # #5 Delete - Eliminar un registre per id
# # @app.delete("/api/products/{id}")
# # async def delete_user(id: int):
# #     users.pop(id-1)
# #     return {"El producte": product "s'ha eliminat correctament"}
#
# # @app.post("/user", response_model=dict, tags=["CREATE"])
# # def addUser(user: UserRequest, db:Session = Depends(get_db)):
# #     insert_user = User.model_validate(user)
# #     db.add(insert_user)
# #     db.commit()
# #     return {"msg":"Afegit usuari correctament"}
# #
# #
# # @app.get("/user/{id}", response_model=UserResponse, tags=["READ by ID"])
# # def getUser(id: int, db:Session = Depends(get_db)):
# #     stmt = select(User).where(User.id == id)
# #     result = db.exec(stmt).first()
# #     print(result) #pa ver lo que se printa
# #     return UserResponse.model_validate(result)
#
