import os
import sys

from  src.Logging import logging
from src.exception import CustomException
from src.utils import save_images
from PIL import Image
from dataclasses import dataclass

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

