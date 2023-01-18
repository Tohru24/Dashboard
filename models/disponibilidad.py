import sqlalchemy
from models.enums import ProductMeasurement, ProductStatus, Dias_de_disponibilidad
from db import metadata


"""
disponibilidades: Es la tabla en donde se almacenaran los datos de las disponibilidades, relaciona el id del usuario 
que la creo
"""
disponibilidad = sqlalchemy.Table(
    "disponibilidades",
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
    sqlalchemy.Column("modificador_id", sqlalchemy.ForeignKey("usuarios.id"), nullable=False),
    sqlalchemy.Column("creador_id", sqlalchemy.ForeignKey("usuarios.id"), nullable=False)

)