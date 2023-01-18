from pydantic import BaseModel
from models.enums import Dias_de_disponibilidad

class Dias_DistribuidorOutModel(BaseModel):
    distribuidor_id: str
    dia: Dias_de_disponibilidad