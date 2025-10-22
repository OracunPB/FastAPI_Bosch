from sqlmodel import SQLModel

class Product(SQLModel, table=True):
    id: int = Field(default=None, )
    name: str
    price: int
