import os
import sys
import pandas as pd
from pathlib import Path
from src.exception import CustomException
from src.Logging import logging
from src.utils import read_answers, read_question
from dataclasses import dataclass
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

@dataclass
class MarkesGenrationConfig:
    markes_path=os.path.join("data","Final_markes.xlsx")

class MarkesGenration:
    def __init__(self):
        self.markes_genration_config_obj = MarkesGenrationConfig()

    def evaluate_answer(self, question: str, answers: list):
        try:
            logging.info("Starting answer evaluation.")
            api = os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=api)
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            chat_model = model.start_chat()
            markes = []

            # Clear prompt to ensure only the score is returned
            prompt = (
                f"Evaluate the following answer to the question provided. If the answer is left blank, consider it as an incomplete response and assign a score of 0 for that particular question. "
                f"Rate the answer only on a scale of 0 to 10 and return just the score in the format 'X/10'.\n\n"
                f"Question: {question}\n\n"
            )

            # Send the initial prompt to start the conversation
            response = chat_model.send_message(prompt)
            response = chat_model.send_message("I will now send you the answers. Please provide the score based only on the above criteria, with an additional comment not more then 10 words")
            student_markes={}
            for i in answers:
                answer = read_answers(i)
                # Send the answer for evaluation
                response = chat_model.send_message(answer)
                score_text = response.text.strip()

                
                markes.append(score_text)
                student_markes[f'{Path(i).stem}']=score_text# Handle empty responses

            print(markes)
            df = pd.DataFrame(list(student_markes.items()), columns=['Student Name', 'Score'])

            # Save the DataFrame to an Excel file
            df.to_excel(self.markes_genration_config_obj.markes_path, index=False)

            print(f"Marks have been saved to {self.markes_genration_config_obj.markes_path}.")# Print the scores list for verification

            return self.markes_genration_config_obj.markes_path
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    a = MarkesGenration()
    questions = read_question(r'D:\END_TO_END_MAJOR\artifacts\Questions.txt')
    path='data'
    answers =[os.path.join(path,file) for file in os.listdir(path) if file.endswith('.txt')]
    a.evaluate_answer(questions, answers)
    # for i in answers:
    #     print(Path(i).stem)
