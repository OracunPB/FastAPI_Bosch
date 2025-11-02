from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi.middleware.cors import CORSMiddleware
from models.Product import Product, ProductRequest, ProductStock, ProductUpdate
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

#1 Create - Afegir un nou registre a la taula
@app.post("/api/product", response_model=dict)
def create_product(product: Product):
    with Session(engine) as db:
        db.add(product)
        db.commit()
        db.refresh(product)
        return {"message": "Producte afegit correctament"}
    
#2 Read - Consultar totes les dades d’UN registre a la taula.
@app.get("/api/product/{id}", response_model=Product)
def get_product_by_id(id: int):
    with Session(engine) as db:
        product = db.get(Product, id)
        return product
    
#3 Read - Consultar totes les dades de tots els registres de la taula.
@app.get("/api/product", response_model=list[Product])
def get_all_products():
    with Session(engine) as db:
        products = db.exec(select(Product)).all()
        return products
    
#4 Read - Consultar les dades filtrant per un camp
@app.get("/api/product/by_field/{field}/{value}", response_model=list[Product])
def get_product_by_field(field: str, value: str):
    with Session(engine) as db:
        query = select(Product)
        
        if field == "name":
            query = query.where(Product.name == value)
        elif field == "category":
            query = query.where(Product.category == value)
        elif field == "price":
            query = query.where(Product.price == int(value))
        elif field == "stock":
            query = query.where(Product.stock == int(value))
        elif field == "sale":
            query = query.where(Product.sale == (value.lower() == "true"))
        else:
            return []
        
        results = db.exec(query).all()
        return results

#5 Delete - Eliminar un registre per id
@app.delete("/api/product/delete/{id}", response_model=dict)
def delete_product(id: int):
    with Session(engine) as db:
        product = db.get(Product, id)
        if not product:
            return {"error": "ID no trobat"}
        db.delete(product)
        db.commit()
        return {"message": f"Producte '{product.name}' eliminat correctament"}
    
#6 Read - Lectura parcial
@app.get("/api/product/stock/list", response_model=list[ProductStock])
def get_stock_only():
    with Session(engine) as db:
        products = db.exec(select(Product)).all()
        return products

#7 Update - Modificació total (PUT)
@app.put("/api/product/{id}", response_model=dict)
def update_product(id: int, updated_data: ProductUpdate):
    with Session(engine) as db:
        product = db.get(Product, id)
        if not product:
            return {"error": "Producte no trobat"}

        product.name = updated_data.name
        product.price = updated_data.price
        product.category = updated_data.category
        product.stock = updated_data.stock
        product.sale = updated_data.sale

        db.add(product)
        db.commit()
        db.refresh(product)
        return {"message": f"Producte {product.name} actualitzat correctament"}

#8 Update - Modificació parcial un camp (PATCH)
@app.patch("/api/product/{id}/stock/{value}", response_model=dict)
def update_product_stock(id: int, value: int):
    with Session(engine) as db:
        product = db.get(Product, id)
        if not product:
            return {"error": "Producte no trobat"}

        product.stock = value
        db.add(product)
        db.commit()
        db.refresh(product)
        return {"message": f"Estoc del producte {product.name} actualitzat a {product.stock}"}

#9 Update - Modificació parcial dos camps
@app.patch("/api/product/{id}/update_partial", response_model=dict)
def update_two_fields(id: int, price: int, stock: int):
    with Session(engine) as db:
        product = db.get(Product, id)
        if not product:
            return {"error": "Producte no trobat"}

        product.price = price
        product.stock = stock

        db.add(product)
        db.commit()
        db.refresh(product)
        return {"message": f"Producte {product.name} actualitzat: preu={product.price}, estoc={product.stock}"}
