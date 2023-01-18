from datetime import date

from pydantic import BaseModel

from models import Dias_de_disponibilidad


class DisponibilidadOut(BaseModel):
    id: int
    producto: str
    cantidad: float
    unidad: str
    status: str
    fecha_de_creacion: date
    fecha_de_disponibilidad: date
    dia_de_disponibilidad: Dias_de_disponibilidad


class DisponibilidadUpdateModelOut(BaseModel):
    cantidad: float
    status: str