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



## Run

- Once cloned, Navigate inside the "pdf_to_h5p_converter" folder using `cd pdf_to_h5p_converter` 
- Copy the PDF that you have to convert into the current folder 
- Then just run `python3 generateh5p.py <pdfFileNameToBeConverted>` 
    For Eg:
        ```
        python3 generateh5p.py lecture.py
        ```
- The program also accepts additional parameters such as `dpi` and `resolution` of the image. The default values are `dpi=600` and `resolution=1920`. If you have to change the parameters, then run using 
```
python3 generateh5p.py Lect02-CompArchi.pdf --dpi 600 --resolution 1920
```
- The h5p file will be generated on the root folder itself.


