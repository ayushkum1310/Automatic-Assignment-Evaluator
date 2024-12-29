import os
import sys
import time
from pathlib import Path
from fastapi.responses import JSONResponse
from src.Logging import logging
from src.exception import CustomException
from src.data_injestion import DataIngestion
from src.image_preprocessing import DataTransformation
from src.text_extraction import TextExtractor
from src.result_compilation import SimilarityScore
from src.markes_genration import MarkesGenration

class Get_data:
    @staticmethod
    async def get_data_for_single_pdf(file, questions_user):
        try:
            # Save uploaded PDF file
            upload_dir = "pdfs"
            os.makedirs(upload_dir, exist_ok=True)
            pdf_path = os.path.join(upload_dir, file.filename)

            # Writing the uploaded file to disk
            with open(pdf_path, "wb") as buffer:
                buffer.write(await file.read())

            # Processing starts
            start_time = time.time()
            file_name = Path(file.filename).stem

            # Data Ingestion
            data_injestion_obj = DataIngestion()  # Assuming DataIngestion does not require config.
            img_path, question = data_injestion_obj.initiate_data_ingestion(pdf_path, questions_user)

            # Data Transformation
            preprocessor_obj = DataTransformation()  # Assuming no need for config here.
            preprocessed_img = preprocessor_obj.initiate_data_transformation(img_path)

            # Text Extraction
            text_extractor_obj = TextExtractor(file_name=file_name)  # Ensure file_name is passed
            extracted_text_path =text_extractor_obj.initiate_text_extraction(preprocessed_img)

            

            # Mark Generation
            marks_genration_obj = MarkesGenration()  # Ensure proper initialization
            marks =  marks_genration_obj.evaluate_answer(question, [extracted_text_path])

            # End processing time
            end_time = time.time()

            # Prepare response
            response = {
                "message": "File processed successfully",
                "time_taken": end_time - start_time,
                "marks": marks
            }

            # Log processing time
            logging.info(f"File processed successfully in {end_time - start_time} seconds")

            # Return a response
            return JSONResponse(content=response)

        except Exception as e:
            logging.error("Error processing file", exc_info=True)
            raise CustomException(e, sys)
