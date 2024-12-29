import os
import sys
from pathlib import Path
from  src.Logging import logging
from src.exception import CustomException
from src.utils import save_images
from PIL import Image
from dataclasses import dataclass
from src.data_injestion import DataIngestion,DataIngestionConfig
@dataclass
class DataTransformationConfig:
    Preprocesser_obj=os.path.join("artifacts","preprocessed_images")
    
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
    def initiate_data_transformation(self,images):
        try:
            #check Wheather the directory exist or not
            logging.info("Preprocessing.py has started")
            logging.info("Checking Directory ")
            
            os.makedirs(os.path.dirname(self.data_transformation_config.Preprocesser_obj),exist_ok=True)
            
            images_per_combined=3
            combined_images = []
            
            logging.info('Staring image Processing........')
            for i in range(0, len(images), images_per_combined):
                # Get the current batch of images
                batch = images[i:i + images_per_combined]
                
                # Determine the maximum width and total height for vertical combining
                widths, heights = zip(*(img.size for img in batch))
                max_width = max(widths)
                total_height = sum(heights)
                
                # Create a new blank image with the determined dimensions
                combined_image = Image.new('RGB', (max_width, total_height))
                
                # Paste the images one below the other
                y_offset = 0
                for img in batch:
                    combined_image.paste(img, (0, y_offset))
                    y_offset += img.height
                
                # Append the combined image to the result list
                combined_images.append(combined_image)
            #Saving result in artifact folder
            logging.info("Preprocessing has been complited Returing The images")
            
            
            # Saving imgaes to artifacts
            save_images(combined_images,self.data_transformation_config.Preprocesser_obj)    
            
            return combined_images
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    pdf_path=Path("D:\END_TO_END_MAJOR\IMG_20240724_221056.pdf")
    Data_injestion_obj=DataIngestion()
    img_path,question=Data_injestion_obj.initiate_data_ingestion(pdf_path,'''Q1. Explain the benefits of ITSM. Define the key perspective of ITSM.
Q2.Analytically discuss the importance of identity and access management in ensuring security & compliance in cloud Environments.
Q3.How does ITSM differs when managing services in the cloud compared to traditional on-premises environment?
Q4.How can organizations ensure compliance and security in cloud services management?
Q5.Explain Resource allocation and its configuration in Cloud Computing environment?
''')
            
            # Creating Data Transformation object and Initiaing the function
    preprocessor_obj=DataTransformation()
    preprocesses_img=preprocessor_obj.initiate_data_transformation(img_path)
    print(preprocesses_img)

