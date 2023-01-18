from pydantic import BaseModel

class Dias_DistribuidorModel(BaseModel):
    dia: int
    usuario: int
