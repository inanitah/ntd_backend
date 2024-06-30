from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import routes

app = FastAPI()

app.include_router(routes.router)

origins = [
    "http://localhost:3001",  # React app's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)