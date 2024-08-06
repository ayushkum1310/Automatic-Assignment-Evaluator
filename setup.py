import os
import sys
 
from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT='-e .'
# Writing a Function to get the requirements fro requirements.txt
def get_requirements(file_path):
    # '''This function will return a list of requirements.
    # '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[ req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    
    
    return requirements  
 

setup(
    name="Automatic Assignment Evaluator",
    version="0.1.0",
    author="Ayush Kumar",
    author_email="ayushpripl@gmil.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')    
)



