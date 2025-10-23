from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    price: int
    stock: int
    sale: bool

class ProductRequest(SQLModel): #Mostra el producte en client view
    name: str
    price: int
    sale: bool

class ProductStock(SQLModel): #Mostra únicament el stock d'un producte
    name: str
    stock: int