from pydantic import BaseModel
from productos import ProductosModel

class Producos_DistribuidorModel(BaseModel):
    user_id: str
    product_id: int