from enum import Enum


class ProductCategory(str, Enum):
    organico = "organico"
    inorganico = "inorganico"


class ProductMeasurement(str, Enum):
    kg = "kilo"
    lb = "libra"


class ProductPackage(str, Enum):
    bolsa = "bolsa"
    caja = "caja"


class ProductStatus(str, Enum):
    sin_modificar = "sin modificar"
    modificado = "modificado"


class UserStatus(str, Enum):
    activo = "activo"
    inactivo = "inactivo"


class RoleType(str, Enum):
    master = "master"
    distribuidor = "distribuidor"


class Dias_de_disponibilidad(str, Enum):
    Lunes = "Lunes"
    Martes = "Martes"
    Miercoles = "Miercoles"
    Jueves = "Jueves"
    Viernes = "Viernes"
    Sabado = "Sabado"
    Domingo = "Domingo"
