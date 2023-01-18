import sqlalchemy

from models.enums import ProductMeasurement, ProductStatus, Dias_de_disponibilidad
from db import metadata


"""
copia_disponibilidades: se encarga de copiar la data de las disponibilidades con la intencion de usarla como data temporal
para mostrar las disponibilidades en el front para los distribuidores.
"""
copia_disponibilidad = sqlalchemy.Table(
    "copia_disponibilidades",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("producto", sqlalchemy.String(60), nullable=False),
    sqlalchemy.Column("categoria", sqlalchemy.String(60), nullable=False),
    sqlalchemy.Column("cantidad", sqlalchemy.Float, nullable=False),
    sqlalchemy.Column("unidad", sqlalchemy.Enum(ProductMeasurement), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.Enum(ProductStatus), nullable=False,
                      server_default=ProductStatus.sin_modificar.name),
    sqlalchemy.Column("fecha_de_creacion", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("fecha_de_modificacion", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("fecha_de_disponibilidad", sqlalchemy.Date, nullable=False),
    sqlalchemy.Column("dia_de_disponibilidad", sqlalchemy.Enum(Dias_de_disponibilidad), nullable=False),
    sqlalchemy.Column("creador_id", sqlalchemy.ForeignKey("usuarios.id"), nullable=False)
)
