import sqlalchemy

from db import metadata

"""
disp_usuario_productos: Se encarga de relacionar los productos que maneja cada usuario
"""
disp_usuario_producto = sqlalchemy.Table(
    "disp_usuario_productos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("producto", sqlalchemy.ForeignKey("productos.id"), nullable=False),
    sqlalchemy.Column("usuario", sqlalchemy.ForeignKey("usuarios.id"), nullable=False)
)
