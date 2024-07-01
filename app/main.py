from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app import routes
from app.database import db_session_middleware

app = FastAPI()

app.include_router(routes.router, prefix="/api/v1")  # If are new version add the routes here

origins = [
    "http://localhost:3000",  # Change to your local env
    "https://ntdfrontend-702d74153fdf.herokuapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to handle database connections
app.middleware("http")(db_session_middleware)

