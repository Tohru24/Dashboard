from typing import List
from fastapi import APIRouter, Depends
from starlette.requests import Request
from managers.disponibilidad import DisponibilidadManager
from managers.master import MasterManager
from schemas.request.dias import DiasModel
from schemas.request.dias_distribuidor import Dias_DistribuidorModel
from schemas.request.productos import ProductosModel
from schemas.request.productos_distribuidor import Producos_DistribuidorModel
from schemas.response.disponibilidad import DisponibilidadOut

router = APIRouter(tags=["Master"])


"""@router.post("/register_Master/", status_code=201)
async def register_master(contraseña: int, user_data: UserRegisterMaster):
    token = await MasterManager.register_master(contraseña, user_data.dict())
    return {"token": token}"""

@router.post("/create_product/")
async def create_product(product_data: ProductosModel):
    return await MasterManager.create_product(product_data.dict())

@router.post("/create_dia/")
async def create_dia(dia_data: DiasModel):
    return await MasterManager.create_dia(dia_data.dict())


@router.post("/dias_distribuidor/")
async def create_dias_for_distribuidor(dia_data: Dias_DistribuidorModel):
    return await MasterManager.create_dia_for_distribuidor(dia_data.dict())


@router.post("/productos_distribuidor")
async def post_product_for_create_dias_for_distribuidor(product_data: Producos_DistribuidorModel):
    return await MasterManager.post_product_for_user(product_data.dict())

