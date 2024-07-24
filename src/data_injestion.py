import os
import sys
from src.Logging import logging
from src.exception import CustomException
from src.image_preprocessing import DataTransformationConfig
from src.image_preprocessing import DataTransformation
from src.text_extraction import TextExtractor,TextExtractorConfig
from src.utils import save_images,save_questions
from dataclasses import dataclass
from pdf2image import convert_from_path
from pathlib import Path
import time
@dataclass
class DataIngestionConfig:
    images: str = os.path.join("artifacts", 'Input_images')
    Q_text: str=os.path.join("artifacts", 'Questions.txt')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self, path,text:str):
        logging.info("Data Ingestion has Started")
        try:
            logging.info("Checking Existence of Directory")
            os.makedirs(os.path.dirname(self.ingestion_config.images), exist_ok=True)
            os.makedirs(os.path.dirname(self.ingestion_config.Q_text), exist_ok=True)
            logging.info("Directory Found to save images")
            
            pdf_file = path
            logging.info("Converting PDf to images >>>>>>>>>>>>>")
            images = convert_from_path(pdf_path=pdf_file)
            
            #Saving images and question 
            save_images(images=images, output_dir=self.ingestion_config.images)
            save_questions(text,self.ingestion_config.Q_text)
            logging.info(f"Sucessfully Converted and save the Image and the question in {self.ingestion_config.images} and {self.ingestion_config.Q_text}")
            return (images,text)
                   
        except Exception as e:
            raise CustomException(e, sys)

# if __name__ == '__main__':
    
#     start_time=time.time()
#     obj = DataIngestion()
    
#     path=Path('D:\END_TO_END_MAJOR\IMG_20240724_221056.pdf')
#     img,text = obj.initiate_data_ingestion(path,"Q1 Who is the hod of sharda")
#     newimg=DataTransformation().initiate_data_transformation(img)
#     a=TextExtractor().initiate_text_extraction(newimg)
#     print(a)
#     print(time.time()-start_time,'This is the time')
