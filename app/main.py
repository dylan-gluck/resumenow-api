from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import parse, format, job

app = FastAPI()

origins = [
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(parse.router)
app.include_router(format.router)
app.include_router(job.router)
