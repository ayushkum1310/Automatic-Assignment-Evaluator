import os

import sys
import time

from src.utils import save_questions
from src.Logging import logging
from src.exception import CustomException


from dataclasses import dataclass
import google.generativeai as genai
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.messages import HumanMessage
# from src.image_preprocessing import DataTransformation
from dotenv  import load_dotenv
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path
load_dotenv()



@dataclass
class TextExtractorConfig:
    text_path=os.path.join("data","text.txt")
    
class TextExtractor:
    def __init__(self) :
        self.text=TextExtractorConfig()
        
    def initiate_text_extraction(self,combined_images):
        try:
            logging.info("Extraction Has started")
            api=os.getenv("GEMINI_API_KEY")                                   
            genai.configure(api_key=api) 
            model=genai.GenerativeModel('gemini-1.5-flash-latest') 
            response_text =""
            for i in range(len(combined_images)):
                response=model.generate_content([combined_images[i],'you are an profesonal tool which return the handwritten text without manupulation from the image without any data loss or manupulation'],stream=False)
                
                response_text += response.text + "\n"
            logging.info("Sucessfully extracted all the text")
            os.makedirs(os.path.dirname(self.text.text_path), exist_ok=True)
            with open(self.text.text_path, "w", encoding="utf-8") as file:
                file.write(response_text)
            logging.info(f"Sucessfully Saved The txt filr at {self.text.text_path} GO check ")
            logging.info("Exiting text_extraction.py")
            return response_text 
            
        except Exception as e:
            raise CustomException(e,sys)
        
  