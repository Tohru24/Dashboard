from pydantic import BaseModel, Field
from models.enums import ProductCategory


class Productos_UsuariosOutModel(BaseModel):
    nombre : str
    categoria : ProductCategory