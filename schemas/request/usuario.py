from typing import Optional
from pydantic import BaseModel
from fastapi import Form, Request
from models import RoleType


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("user_id")
        self.password = form.get("password")


class RegisterForm(BaseModel):
    user_id: str = Form(...)
    password: str = Form(...)
    role: RoleType = Form(...)
