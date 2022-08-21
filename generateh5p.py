import json
import copy
import os
import random
import string
from os import listdir
from os.path import isfile,join
import subprocess
import shutil
import time
import sys
import uuid
from pathlib import Path


if __name__ == "__main__":
    """
    This module is used to convert the given pdf slides into the h5p package

Example:
    To run the file, please use the following command:

        $ python generateh5p.py <inputfilename> --dpi 300 --resolution 1920
    
The last two parameters (dpi) and resolution are non mandatory values 

Defaults:
    The value DPI defaults to 600 and the resolutiion defaults to 1920



Todo:
    * Add Support for Adding interactive quizzes 


"""

    if(len(sys.argv) <= 1):
        print("Please enter the Input Argument as the name of PDF file")
        exit(0)
    elif(len(sys.argv) <=2):
        inputFileName = sys.argv[1]
        DPI = 600
        pixel = 1920
    else:
        inputFileName = sys.argv[1]
        for i in range(2,len(sys.argv)):
            if(sys.argv[i] == "--dpi"):
                DPI = int(sys.argv[i+1])
            elif(sys.argv[i] == "--resolution"):
                pixel = int(sys.argv[i+1])
    ## GLOBAL VARIABLES 
    
    Title = Path(inputFileName).stem
    OPFileName = Path(inputFileName).stem

    with open ("contentBase/content.json","r") as f:
        jsonData = json.load(f)
    JsonDataCopy = copy.deepcopy(jsonData)

    ## get Copy of one Slide
    SlideDataBase = copy.deepcopy(jsonData['presentation']['slides'][0])

    ## remove content directory
    dirpath = Path('.')/'content'
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree('content')

    ## make a new content directory
    os.system("mkdir -p content")
    os.system("mkdir -p content/images")

    p1 = subprocess.call("mkdir -p content".split(" ")) 

    p1 = subprocess.call("mkdir -p content/images".split(" ")) 


    ## Extract all the image files to Folder images
    # Copy the PDF to the content folder 
    p1 = subprocess.call(f'cp {inputFileName} content/images/'.split(" ")) 


    ## Extract all the pdf as images
    p1 = subprocess.call(f'pdftoppm -png -r {DPI} -scale-to {pixel} {inputFileName} image-{Title}'.split(" "), cwd="content/images/") 


    ## Delete pdf file
    p1 = subprocess.call(f'rm content/images/{inputFileName}'.split(" ")) 



    ## Extract Image Files 
    imageFiles = [f for f in listdir("content/images/") if isfile(join("content/images/",f))]

    ## remove base slide data from main json data 
    ## the copy is available in SliSlideDataBase

    del jsonData['presentation']['slides'][0]


    ## create a new folder and copy contents over there 
    p1 = subprocess.call(f'cp -r BaseTemplate/ {OPFileName}'.split(" "))

    ## Sort them Alphabeticallty
    imageFiles.sort()

    print("Converting the PDF File into h5p..!")


    ## Create a Slide for each image 
    for image in imageFiles:
        currSlide = copy.deepcopy(SlideDataBase)
        currSlide['elements'][0]['action']['params']['file']['path'] = f"images/{image}"
        currSlide['elements'][0]['action']['subContentId'] = str(uuid.uuid4())

        jsonData['presentation']['slides'].append(currSlide)



    ## Write the current json to content folder 
    with open("content/content.json" , 'w') as f:
        json.dump(jsonData,f)

    ## copy to the OOP folder 
    p1 = subprocess.call(f'cp -r content/ {OPFileName}/'.split(" "))


    ## make zip file 
    shutil.make_archive(OPFileName, 'zip', OPFileName)

    ## rename to h5p 
    p1 = subprocess.call(f'mv {OPFileName}.zip {OPFileName}.h5p'.split(" "))

    ## remove folder 
    p1 = subprocess.call(f'rm -r {OPFileName}/'.split(" "))

    print(f"[ Message: ] {OPFileName}.h5p Successfully generated")
