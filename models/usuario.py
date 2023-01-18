import sqlalchemy

from models.enums import RoleType, UserStatus
from db import metadata

"""
usuarios: Almacena a todos los usuarios del programa
"""
usuario = sqlalchemy.Table(
    "usuarios",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String(30), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("role", sqlalchemy.Enum(RoleType), nullable=False),
    sqlalchemy.Column("status", sqlalchemy.Enum(UserStatus), nullable=False
                      , server_default=UserStatus.activo.name)
)
