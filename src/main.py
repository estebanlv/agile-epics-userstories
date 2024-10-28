from fastapi import FastAPI
from src.routers import generate
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Epic to User Stories Generator")

# Include the router
app.include_router(generate.router)

# Mount static files
app.mount("/src/static", StaticFiles(directory="src/static"), name="static")

# (Optional) Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
