from fastapi import FastAPI, File, UploadFile, Form,APIRouter
from fastapi.responses import JSONResponse
import os
import time
import sys
from pathlib import Path
from src.Logging import logging
from src.exception import CustomException
from src.data_injestion import DataIngestion
from src.image_preprocessing import DataTransformation
from src.text_extraction import TextExtractor
from src.result_compilation import SimilarityScore
from src.markes_genration import MarkesGenration
from controller.get_data_controller import Get_data
from fastapi.middleware.cors import CORSMiddleware


analytics=Get_data()
analytics_router = APIRouter()



@analytics_router.post("/get-marks-for-single-pdf/",description="This endpoint is used to get the marks for a single pdf file")
async def upload_file(
    file: UploadFile = File(...),
    questions: str = Form(...)
):
    try:
        return await analytics.get_data_for_single_pdf(file,questions)
    except Exception as e:
        raise CustomException(e,sys)
    
@analytics_router.post("/get-text-for-single-pdf/",description="This endpoint is used to get the text for a single pdf file")
async def get_text_for_single_pdf(
    file: UploadFile = File(...)
    
):
    try:
        return await analytics.get_text_for_single_pdf(file)
    except Exception as e:
        raise CustomException(e,sys)
