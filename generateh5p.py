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

    ##Get  Home Path 
    import os 
    home_dir_path = os.getcwd()

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

    home_dir_path = os.getcwd()
    contentPath = os.path.join(home_dir_path,"content")
    imagePath = os.path.join(contentPath,"images")


    with open (f"{home_dir_path}/contentBase/content.json","r") as f:
        jsonData = json.load(f)
    JsonDataCopy = copy.deepcopy(jsonData)

    ## get Copy of one Slide
    SlideDataBase = copy.deepcopy(jsonData['presentation']['slides'][0])

    ## remove content directory
    dirpath = contentPath
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        shutil.rmtree('content')

    ## make a new content directory

    p1 = subprocess.call(f"mkdir -p {contentPath}".split(" ")) 

    p1 = subprocess.call(f"mkdir -p {imagePath}".split(" ")) 


    ## Extract all the image files to Folder images
    # Copy the PDF to the content folder 
    p1 = subprocess.call(f'cp {inputFileName} {imagePath}'.split(" ")) 


    ## Extract all the pdf as images
    p1 = subprocess.call(f'pdftoppm -png -r {DPI} -scale-to {pixel} {inputFileName} image-{Title}'.split(" "), cwd=imagePath) 


    ## Delete pdf file
    p1 = subprocess.call(f'rm {imagePath}/{inputFileName}'.split(" ")) 



    ## Extract Image Files 
    imageFiles = [f for f in listdir(f"{imagePath}") if isfile(join(imagePath,f))]

    # print(imageFiles)

    imageFilesRenamed = []
    ## rename the images with hashes at end
    for index,img in enumerate(imageFiles):
        k = str(uuid.uuid4())[:8]
        filename, file_extension = os.path.splitext(img)
        # print(f"mv {imagePath}/{filename}{file_extension}  {imagePath}/{filename}-{k}{file_extension}")
        # print(img)
        p1 = shutil.move(f'{imagePath}/{filename}{file_extension}', f'{imagePath}/{filename}-{k}{file_extension}')
        
        img = f"{filename}-{k}{file_extension}"
        imageFilesRenamed.append(img)
    
    
    ## remove base slide data from main json data 
    ## the copy is available in SliSlideDataBase
    del jsonData['presentation']['slides'][0]


    ## create a new folder and copy contents over there 
    p1 = subprocess.call(f'cp -r {home_dir_path}/BaseTemplate/ {OPFileName}'.split(" "))

    ## Sort them Alphabeticallty
    imageFilesRenamed.sort()

    print("Converting the PDF File into h5p..!")


    ## Create a Slide for each image 
    for image in imageFilesRenamed:
        currSlide = copy.deepcopy(SlideDataBase)
        currSlide['elements'][0]['action']['params']['file']['path'] = f"images/{image}"
        currSlide['elements'][0]['action']['subContentId'] = str(uuid.uuid4())

        jsonData['presentation']['slides'].append(currSlide)



    ## Write the current json to content folder 
    with open(f"{contentPath}/content.json" , 'w') as f:
        json.dump(jsonData,f)

    ## copy to the OOP folder 
    p1 = subprocess.call(f'cp -r {contentPath}/ {OPFileName}/'.split(" "))


    ## make zip file 
    shutil.make_archive(OPFileName, 'zip', OPFileName)

    ## rename to h5p 
    p1 = subprocess.call(f'mv {OPFileName}.zip {OPFileName}.h5p'.split(" "))

    ## remove folder 
    p1 = subprocess.call(f'rm -r {OPFileName}/'.split(" "))


    os.chdir(home_dir_path)

    print(f"[ Message: ] {OPFileName}.h5p Successfully generated")
