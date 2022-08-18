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

import yaml


if __name__ == "__main__":
    ## GLOBAL VARIABLES 
    inputFileName  = "Lect02-CompArchi.pdf"
    Title = "DS226_Lecture-2"
    OPFileName = "Lecture2"


    ## Read Yaml files 
    with open ("parameters.yaml" , "r") as f:
        param = yaml.safe_load(f)

    ## assign Parameter Values 
    inputFileName = param["Input_PDF_File_Name"] 
    Title = param["Prefix_for_Image_Storage"] 
    OPFileName = param["Output_h5p_file_name"]
    DPI = param["DPI_of_Image"]
    pixel = param["pixelLength"]



    with open ("contentBase/content.json","r") as f:
        jsonData = json.load(f)
    JsonDataCopy = copy.deepcopy(jsonData)

    ## get Copy of one Slide
    SlideDataBase = copy.deepcopy(jsonData['presentation']['slides'][0])

    ## remove content directory
    shutil.rmtree('content')

    ## make a new content directory
    os.system("mkdir -p content")
    os.system("mkdir -p content/images")

    p1 = subprocess.call("mkdir -p content".split(" ")) 

    p1 = subprocess.call("mkdir -p content/images".split(" ")) 



    ## Generate  Substring 
    def generateSubContentID():
        lenStr = [8,4,4,4,12]
        mainStr= ""
        for count,i in enumerate(lenStr):
            k = ''.join(random.choices(string.ascii_lowercase + string.digits, k=i))
            if(count != 0):
                mainStr += "-"+k
            else:
                mainStr = k
        return mainStr


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


    imageFiles.sort()
    ## Create a Slide for each image 
    for image in imageFiles:
        print("-------------------------------------")
        print(image)
        print(currSlide)

        currSlide = copy.deepcopy(SlideDataBase)
        currSlide['elements'][0]['action']['params']['file']['path'] = f"images/{image}"
        currSlide['elements'][0]['action']['subContentId'] = generateSubContentID()

        jsonData['presentation']['slides'].append(currSlide)

        print(currSlide)


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
