from datetime import date

from pydantic import BaseModel, Field
from models import Dias_de_disponibilidad, ProductStatus, ProductMeasurement


class DisponibilidadModel(BaseModel):
    producto: str = Field(..., min_length=3, max_length=60)
    categoria: str = Field(..., min_length=3, max_length=60)
    cantidad: float = Field(..., gt=0)
    unidad: ProductMeasurement = Field(...)
    status: ProductStatus
    fecha_de_creacion: date = Field(...)
    fecha_de_modificacion: date = Field(...)
    fecha_de_disponibilidad: date = Field(...)
    dia_de_disponibilidad: Dias_de_disponibilidad = Field(...)


class DisponibilidadUpdateModel(BaseModel):
    #modificador_id: int
    cantidad: float
    status: str

