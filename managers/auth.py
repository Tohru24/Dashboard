import jwt
from typing import Optional
from asyncpg import UniqueViolationError
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config
from fastapi import HTTPException, Request

from db import database
from models import usuario

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


class AuthManager:

    @staticmethod
    async def register(user_data):
        user_data["password"] = get_password_hash(user_data["password"])
        try:
            id_ = await database.execute(usuario.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "Ya existe un usuario con este user_id")
        user_do = await database.fetch_one(usuario.select().where(usuario.c.id == id_))
        return AuthManager.create_access_token(user_do)

    @staticmethod
    def create_access_token(user, expires_delta: Optional[timedelta] = None):
        username = user["user_id"]
        user_id = user["id"]
        role = user["role"]
        encode = {"sub": username, "id": user_id, "role": role}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        encode.update({"exp": expire})
        return jwt.encode(encode, config("SECRET_KEY"), algorithm="HS256")

    @staticmethod
    async def authenticate_user(username: str, password: str):
        user_do = await database.fetch_one(usuario.select().where(usuario.c.user_id == username))
        if not user_do:
            return False
        if not verify_password(password, user_do["password"]):
            return False
        return user_do

    @staticmethod
    async def get_current_user(request: Request):
        try:
            token = request.cookies.get("access_token")
            if token is None:
                return None
            payload = jwt.decode(token, config("SECRET_KEY"), algorithms=["HS256"])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            role: str = payload.get("role")
            if username is None or user_id is None:
                return None
            return {"username": username, "id": user_id, "role": role}
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return None



