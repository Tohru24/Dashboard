from fastapi import HTTPException
from db import database
from managers.auth import AuthManager
from models import producto, dias, disp_dias_de_distribuidor, usuario,disp_usuario_producto
from models.enums import RoleType
from passlib.context import CryptContext
from sqlalchemy import and_

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class MasterManager:

    @staticmethod
    async def register_master(contraseña, user_data):
        user_data["role"] = RoleType.master
        if contraseña == 123:
            return await AuthManager.register(user_data)
        else:
            raise HTTPException(400, "Token invalido abrase")

    @staticmethod
    async def create_product(product_data):
        id_ = await database.execute(producto.insert().values(product_data))
        return await database.fetch_one(producto.select().where(producto.c.id == id_))

    @staticmethod
    async def create_dia(dias_data):
        id_ = await database.execute(dias.insert().values(dias_data))
        return await database.fetch_one(dias.select().where(dias.c.id == id_))


    @staticmethod
    async def post_product_for_user(product_data):
        product_exists = await database.fetch_one(
            producto.select().where(producto.c.id == product_data["producto"])
        )
        user_exists = await database.fetch_one(
            usuario.select().where(usuario.c.id == product_data["usuario"])
        )
        if product_exists and user_exists:
            id_ = await database.execute(disp_usuario_producto.insert().values(product_data))
            return await database.fetch_one(
                disp_usuario_producto.select().where(disp_usuario_producto.c.id == id_))
        else:
            return None

    @staticmethod
    async def create_dia_for_distribuidor(dia_data):
        dupli = await database.fetch_one(
            disp_dias_de_distribuidor.select().where(disp_dias_de_distribuidor.c.dia == dia_data["dia"])
        )

        dia_exists = await database.fetch_one(
            dias.select().where(dias.c.id == dia_data["dia"])
        )
        user_exists = await database.fetch_one(
            usuario.select().where(usuario.c.id == dia_data["usuario"])
        )
        if dia_exists and user_exists and not dupli:
            id_ = await database.execute(disp_dias_de_distribuidor.insert().values(dia_data))
            return await database.fetch_one(
                disp_dias_de_distribuidor.select().where(disp_dias_de_distribuidor.c.id == id_))
        else:
            return None