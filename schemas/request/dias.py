from pydantic import BaseModel
from models.enums import Dias_de_disponibilidad
class DiasModel(BaseModel):
    dia: Dias_de_disponibilidad