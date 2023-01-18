import sqlalchemy

from db import metadata

"""
dias: Contiene los dias de la semana que seran usados para asignar dias de publicacion de disponibilidades
    para los distribuidores
"""
dias = sqlalchemy.Table(
    "dias",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("dia", sqlalchemy.String(15), unique=True, nullable=False),
)
