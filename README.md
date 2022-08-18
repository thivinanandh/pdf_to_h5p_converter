# PDF to h5p Converter 

This code is used to convert the PDF files into a h5p interactive slide for uploading it to learning management sites like moodle 


## Prerequisites 

To use the code you might need the following packages 
- `pdftoppm`   ( can install using `sudo apt-get install pdftoppm` on Ubuntu/Debian based versions)
- python3
- pyyaml ( python package for yaml files , can install it using `pip install pyyaml`)

## Installation

There is no specifix installation instructions for the same. Just clone the code using 
` git clone https://github.com/thivinanandh/pdf_to_h5p_converter.git` 


## Input Parameter Files
The parameters.yaml file has the following parameters. 

- `Input_PDF_File_Name`        - The name of the PDF file that you have to convert into h5p ( make sure that the pdf file is present in the root directory of the folder. )
- `Prefix_for_Image_Storage`   - The prefix string which you want the images to be saved after extracted from the pdf conversion process.   ( For Eg: If value is "lec" , then images will be named as "lec01.png","lec02.png" and so and so )
- `Output_h5p_file_name`       - The name of the output file to be generated 
- `DPI_of_Image`               - DPI Quality of the image to be rendered from the pdf   ( adjust only if necessary )
- `pixelLength`                - The final width of the image on slide ( adjust only if necessary )
- 
## Run

- Once cloned, Navigate inside the "pdf_to_h5p_converter" folder using `cd pdf_to_h5p_converter` 
- Copy the PDF that you have to convert into the current folder 
- Edit the `parameters.yaml` file as per your configuration 
- Then just run `python3 generateh5p.py` 
- The h5p file will be generated on the root folder itself.


