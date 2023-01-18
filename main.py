from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from db import database
from resources.routes import api_router


app = FastAPI()
app.include_router(api_router)
app.mount("/front/static", StaticFiles(directory="front/static"), name="static")

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



