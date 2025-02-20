from fastapi import FastAPI

from .routers import parse, format

app = FastAPI()

app.include_router(parse.router)
app.include_router(format.router)
