from pydantic import BaseModel


class Producos_DistribuidorOutModel(BaseModel):
    user_id: str
    product_id: int