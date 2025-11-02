from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: int
    category: str
    stock: int
    sale: bool

class ProductRequest(SQLModel): #Mostra el producte en client view
    name: str
    price: int
    category: str
    sale: bool

class ProductStock(SQLModel): #Mostra únicament el stock d'un producte
    name: str
    stock: int
    category: str

class ProductUpdate(SQLModel): #Editar un producte sense veure ID
    name: str
    price: int
    category: str
    stock: int
    sale: bool