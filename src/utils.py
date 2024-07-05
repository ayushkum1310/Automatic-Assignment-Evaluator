from PIL import Image
import os
import os
import sys
from src.Logging import logging
from src.exception import CustomException
# from src.utils import save_images
# from dataclasses import dataclass
# from pdf2image import convert_from_path

def save_images(images, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, img in enumerate(images):
        # Define the path to save the image
        image_path = os.path.join(output_dir, f'image_{i+1}.png')
        # Save the image
        img.save(image_path)

def save_questions(text,path):
    try:
        with open(path,"w",encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        raise CustomException(e,sys)

