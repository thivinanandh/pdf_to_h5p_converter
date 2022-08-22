import os
from flask import Flask, render_template, request,send_file
import os
# import cv2
import base64
import json
import subprocess





app = Flask(__name__,static_url_path='', 
            static_folder='static')

##Global variable for fileName
Global_H5pFileName = ""
Global_ConversionSuccessfull = ""

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods = ['GET','POST'])
def download():
    if request.method == 'POST':
       path = f"{Global_H5pFileName}"
    return send_file(path, as_attachment=True)
    


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    global Global_H5pFileName
    if request.method == 'POST':
        pdf = request.files['my_pdf_file']
        filename, file_extension = os.path.splitext(pdf.filename)
        print(f'{file_extension=}')
        p1 = subprocess.call(f"rm *.pdf".split(" ")) 
        p1 = subprocess.call(f"rm *.h5p".split(" ")) 
        pdf.save(f"{filename}{file_extension}")
        print(f"{filename}{file_extension}")
        dpi = request.form['dpi']
        res = request.form['resolution']
        p1 = subprocess.call(f"python3 generateh5p.py {filename}{file_extension}  --dpi {dpi} --resolution {res}".split(" ")) 

        number = 1 ## Place Holder for the Render script 
        Global_H5pFileName = f"{filename}.h5p"
        
    return render_template("index.html", prediction = number, file_name = Global_H5pFileName)






if __name__ == "__main__":
    app.run(debug=True)
    