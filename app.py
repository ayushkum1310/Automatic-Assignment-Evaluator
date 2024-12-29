from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from controller.get_data_controller import Get_data
from src.exception import CustomException
from fastapi.middleware.cors import CORSMiddleware
from routes.get_data import analytics_router as Analytics_Router
import sys

app = FastAPI()
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

@app.get("/health-check")
def healthCheck():
    return {"message": f"ai-ml server x3 is healthy and running"}


