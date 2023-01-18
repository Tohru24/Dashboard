import datetime
from typing import Optional

from datetime import datetime
from db import database
from models import disponibilidad, RoleType, disp_dias_de_distribuidor, dias, copia_disponibilidad, \
    disp_usuario_producto, producto,usuario


class DisponibilidadManager:
    """
    get_all_disponibilidades: Funcion unica para el master que le regresara
    todas las disponibilidades de la base de datos.
    """

    @staticmethod
    async def get_all_disponibilidades(user):
        if user["role"] == RoleType.master:
            q = disponibilidad.select()
        else:
            q1 = copia_disponibilidad.select().where(copia_disponibilidad.c.creador_id == user["id"])
            q2 = (
                disp_dias_de_distribuidor.select()
                .select_from(disp_dias_de_distribuidor.join(dias))
                .where(usuario.c.id == user["id"])
                .with_only_columns([dias.c.dia])
            )
            q3 = (
                disp_usuario_producto.select()
                .select_from(disp_usuario_producto.join(producto))
                .where(usuario.c.id == user["id"])
                .with_only_columns([producto.c.nombre])
            )
            disponibilidades = await database.fetch_all(q1)
            dias_disp = await database.fetch_all(q2)
            current_date = datetime.now().date()
            productos = await database.fetch_all(q3)
            return disponibilidades, dias_disp, current_date,productos
        return await database.fetch_all(q)

    """
    get_data_for_distribuidor: Retorna toda la informacion necesaria (disponibilidades) y 
    las fechas en las que los distribuidores pueden publicar disponibilidad.
    """

    @staticmethod
    async def get_data_for_post_disponibiliad(user):
        q1 = (
            disp_usuario_producto.select()
            .select_from(disp_usuario_producto.join(producto))
            .where(usuario.c.id == user["id"])
            .with_only_columns([producto.c.nombre])
        )
        q2 = (
            disp_dias_de_distribuidor.select()
            .select_from(disp_dias_de_distribuidor.join(dias))
            .where(usuario.c.id == user["id"])
            .with_only_columns([dias.c.dia])
        )
        dias_disponibles = await database.fetch_all(q1)
        productos_disponibles = await database.fetch_all(q2)
        return dias_disponibles, productos_disponibles

    """
    create_disponibilidad: está funcion sirve para crear una disponibilidad
    """

    @staticmethod
    async def create_disponibilidad(disp_data, user):
        disp_data["creador_id"] = user["id"]
        disp_data["modificador_id"] = user["id"]
        id_ = await database.execute(disponibilidad.insert().values(disp_data))
        return await database.fetch_one(disponibilidad.select().where(disponibilidad.c.id == id_))

    """
    update_disponibilidad: está funcion sirve para actualizar una disponibilidad
    """

    @staticmethod
    async def update_disponibilidad(order_id, updated_data, user):
        updated_data["modificador_id"] = user["id"]
        q = disponibilidad.update().where(disponibilidad.c.id == order_id)
        await database.execute(q.values(updated_data))
        return await database.fetch_one(disponibilidad.select().where(disponibilidad.c.id == order_id))
