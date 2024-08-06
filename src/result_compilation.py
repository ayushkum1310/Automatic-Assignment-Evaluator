import os
import sys
from pathlib import Path
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from src.Logging import logging
from src.exception import CustomException
from dataclasses import dataclass

@dataclass
class Similaritymatrixconfig:
    matrix_path=os.path.join("data","similarity_score.xlsx")
    
class SimilarityScore:
    def __init__(self):
        self.similarity_config_obj=Similaritymatrixconfig()
    def initiate_similarity_score(self,files:list):
        try:
            logging.info("Result Compilation has started in this we are calculating similarity score")
            assignments:list=[]
            student_names:list=[]
            for file in files:
                with open(file,'r',encoding='utf-8') as f:
                    assignments.append(f.read())
                    student_names.append(os.path.basename(file))
            vectorizer=TfidfVectorizer()
            Tfidf_matrix=vectorizer.fit_transform(assignments)
            
            cosine_sim=cosine_similarity(Tfidf_matrix)
            
            Similarity_df=pd.DataFrame(cosine_sim,index=student_names,columns=student_names)
            
            Similarity_df.to_excel(self.similarity_config_obj.matrix_path)
            return self.similarity_config_obj.matrix_path                
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    try:
        a=SimilarityScore()
        path='data'
        b=[]
        file_paths=[os.path.join(path,file) for file in os.listdir(path) if file.endswith('.txt')]
        hui=a.initiate_similarity_score(files=file_paths)
        print(hui)
           
                
        print(b)
                
            
       
    except Exception as e:
        raise CustomException(e,sys)
