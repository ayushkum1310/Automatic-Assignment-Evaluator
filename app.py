from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from controller.get_data_controller import Get_data
from src.exception import CustomException
from fastapi.middleware.cors import CORSMiddleware
from routes.get_data import analytics_router as Analytics_Router
from routes.login import login_router
import sys
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Ensure the "data" directory exists
data_dir = os.path.abspath("data")  # Get the absolute path of the "data" directory
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Mount the "data" directory to serve static files
app.mount("/data", StaticFiles(directory=data_dir), name="data")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can specify domains instead of "*")
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {"message": "Server is running"}



app.include_router(Analytics_Router, tags=["Analytics"], prefix="/analytics")
app.include_router(login_router, tags=["Login"], prefix="/login")

@app.get("/health-check")
def health_check():
    return {"message": "Server is healthy and running"}


