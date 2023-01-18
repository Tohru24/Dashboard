import sqlalchemy

from db import metadata
from models.enums import ProductCategory


"""
productos: Almacena los productos con categoria disponibles
"""
producto = sqlalchemy.Table(
    "productos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nombre", sqlalchemy.String(60), unique=True, nullable=False),
    sqlalchemy.Column("categoria", sqlalchemy.Enum(ProductCategory), nullable=False)
)