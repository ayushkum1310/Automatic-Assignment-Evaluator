import os
import sys
import time
from src.utils import save_questions
from src.Logging import logging
from src.exception import CustomException
from dataclasses import dataclass
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path

load_dotenv()

@dataclass
class TextExtractorConfig:
    text_path: str
    
class TextExtractor:
    def __init__(self, file_name: str):
        self.text = TextExtractorConfig(text_path=os.path.join('data', f"{file_name}_text.txt"))
    def initiate_text_extraction(self, combined_images):
        try:
            logging.info("Extraction Has started")
            api = os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=api)
            model = genai.GenerativeModel('gemini-2.0-flash-lite')
            # Refined Prompt for Better Accuracy
            # prompt = (
            #     'you are an profesonal tool which return the handwritten text without manupulation from the image without any data loss or manupulation'
            # )
            prompt = (
                'Precisely extract only the handwritten text from this image. Do not interpret, add, rephrase, or omit any content, symbols, punctuation, or formatting. Each character, line, and spacing must match exactly what is visible in the image, with no additional or modified content. Provide an exact digital replication of the handwritten text as it appears in the image.'
            )
            response_text = ""
            for image in combined_images:
                response = model.generate_content([image, prompt], stream=False)
                
                response_text += response.text.strip() + "\n"

            logging.info("Successfully extracted all the text")
            os.makedirs(os.path.dirname(self.text.text_path), exist_ok=True)
            with open(self.text.text_path, "w", encoding="utf-8") as file:
                file.write(response_text)
                
            logging.info(f"Successfully saved the text file at {self.text.text_path}. Check it out!")
            logging.info("Exiting text_extraction.py")
            return self.text.text_path
            
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_text_extraction_for_single_pdf(self,combined_images):
        try:
            logging.info("Extraction Has started")
            api = os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=api)
            model = genai.GenerativeModel('gemini-2.0-flash-lite')#gemini-1.5-pro-latest
            prompt = (
                'Precisely extract only the handwritten text from this image. Do not interpret, add, rephrase, or omit any content, symbols, punctuation, or formatting. Each character, line, and spacing must match exactly what is visible in the image, with no additional or modified content. Provide an exact digital replication of the handwritten text as it appears in the image.'
            )
            response_text = ""
            for image in combined_images:
                response = model.generate_content([image, prompt], stream=False)    
                response_text += response.text.strip() + "\n"
                
            logging.info("Successfully extracted all the text")
            
            return response_text
        
        except Exception as e:
            raise CustomException(e, sys)
        
# if __name__ == '__main__':
#     from src.data_injestion import DataIngestion, DataIngestionConfig  # 👈 move here
#     from src.image_preprocessing import DataTransformation,DataTransformationConfig
#     start_time = time.time()
#     obj = DataIngestion()

#     path = Path(r'D:\END_TO_END_MAJOR\IMG_20240724_221056.pdf')
#     img, text = obj.initiate_data_ingestion(path, "Q1 Who is the hod of sharda")
#     newimg = DataTransformation().initiate_data_transformation(img)
#     a = TextExtractor("IMG_20240724_221056").initiate_text_extraction_for_single_pdf(newimg)
#     print(a)
#     print(time.time() - start_time, 'This is the time')

