from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from database import create_db_and_tables
from routers import api, pages

app = FastAPI(title="SERENA UCatólica", version="2.0.0")

app.add_middleware(SessionMiddleware, secret_key="clave-serena-universidad-catolica")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(pages.router)
app.include_router(api.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
