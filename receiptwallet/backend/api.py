from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .routes import token, users, groups

from .db.base import Base
from .db.get_db import engine

app = FastAPI()

app.include_router(token.router)
app.include_router(users.router)
app.include_router(groups.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(engine)


@app.get("/")
def main():
    return HTMLResponse("Hello world")
