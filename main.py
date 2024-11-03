import os
import sys
import time
from pathlib import Path
from src.Logging import logging
from src.exception import CustomException
from src.data_injestion import DataIngestion,DataIngestionConfig
from src.image_preprocessing import DataTransformation,DataTransformationConfig
from src.text_extraction import TextExtractor,TextExtractorConfig

if __name__=="__main__":
    try:
        # Initializing current time
        start_time=time.time()
        
        # Defining path of csv
        pdf_path=Path(r'D:\END_TO_END_MAJOR\pdfs\assignment_CTV5.pdf')
        
        file_name=pdf_path.stem
        # Creating Data injestion object and Initiaing the function
        Data_injestion_obj=DataIngestion()
        img_path,question=Data_injestion_obj.initiate_data_ingestion(pdf_path,"Will data company come for placement in shards")
        
        # Creating Data Transformation object and Initiaing the function
        preprocessor_obj=DataTransformation()
        preprocesses_img=preprocessor_obj.initiate_data_transformation(img_path)
        
        # Creating Data Extractor object and Initiaing the function
        text_extractor_obj=TextExtractor(file_name=file_name)
        text_file_path:list=[]
        extracted_tect_path=text_extractor_obj.initiate_text_extraction(preprocesses_img)
        text_file_path.append(extracted_tect_path)
        
        # Printng The time required for The whole process
        print(time.time()-start_time,'Time taken ')
        logging.info("The process of text Extraction and Document Making Has been completed")
        logging.info(f'Time taken to Digitize the Document is {time.time()-start_time} Sec')
    except Exception as e:
        raise CustomException(e,sys)