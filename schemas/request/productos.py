from pydantic import BaseModel
from models.enums import ProductCategory


class ProductosModel(BaseModel):
    nombre : str
    categoria : ProductCategory