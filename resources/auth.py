from fastapi import APIRouter, Depends,Request, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from managers.auth import AuthManager
from starlette import status
from schemas.request.usuario import LoginForm, RegisterForm
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(prefix="/auth",
                   tags=["auth"],
                   responses={401:{"user":"Not authorized"}}
                   )

templates = Jinja2Templates(directory="front/static/templates")

@router.post("/register")
async def register_user(response: Response, form_data: RegisterForm):
    user = await AuthManager.register(form_data.dict())
    return user


@router.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await AuthManager.authenticate_user(form_data.username, form_data.password)
    if not user:
        return False
    token_expires = timedelta(minutes=120)
    token = AuthManager.create_access_token(user,expires_delta=token_expires)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})


@router.post("/", response_class=HTMLResponse)
async def login(request:Request):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/disponibilidad", status_code=status.HTTP_302_FOUND)

        validate_user_cookie = await login_for_access_token(response=response, form_data=form)
        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request":request, "msg":msg})
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request":request, "msg":msg})

@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response