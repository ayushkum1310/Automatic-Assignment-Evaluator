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
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
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
