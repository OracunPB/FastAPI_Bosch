from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi.middleware.cors import CORSMiddleware
from models.Product import Product, ProductRequest, ProductStock
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

# Create - Afegir un nou registre a la taula
@app.post("/api/product")
def create_product(product: Product):
    with Session(engine) as db:
        db.add(product)
        db.commit()
        db.refresh(product)
        return {"message": "Producte afegit correctament"}
    
# Read - Consultar totes les dades d’UN registre a la taula.
@app.get("/api/product/{id}")
def get_product_by_id(id: int):
    with Session(engine) as db:
        product = db.get(Product, id)
        return product