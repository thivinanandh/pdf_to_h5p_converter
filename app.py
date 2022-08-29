from glob import glob
import os
from flask import Flask, render_template, request,send_file, url_for,send_from_directory
import os
# import cv2
import base64
import json
import subprocess
from werkzeug.utils import secure_filename





app = Flask(__name__,static_url_path='', 
            static_folder='static')

uploads_dir = os.path.join(app.instance_path, 'uploads')
print(f'{uploads_dir=}')
os.makedirs(uploads_dir, exist_ok=True)

app.config['UPLOAD_FOLDER'] = uploads_dir
app.config['h5pName'] = ""

##Global variable for fileName
Global_H5pFileName = ""
Global_ConversionSuccessfull = ""
Global_h5pBasefile = ""

@app.route("/")
def index():
    app.config['UPLOAD_FOLDER'] = uploads_dir
    ### delete all files in the uploads_dir
    p1 = subprocess.call(f"rm {uploads_dir}/*.pdf".split(" ")) 
    p1 = subprocess.call(f"rm {uploads_dir}/*.h5p".split(" ")) 
    return render_template("index.html")


# @app.route("/download", methods = ['GET','POST'])
# global
# def download():
#     if request.method == 'POST':
#        path = f"{Global_H5pFileName}"
#     return send_file(path, as_attachment=True)
    


@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
    global Global_H5pFileName
    global Global_h5pBasefile
    if request.method == 'POST':
        pdf = request.files['my_pdf_file']
        filename, file_extension = os.path.splitext(pdf.filename)
        Global_h5pBasefile = filename
        print(f'{file_extension=}')
        print(f"Current working Directory : {os.getcwd()}")
        print(f"{os.listdir(os.getcwd())=}") 
        # p1 = subprocess.call(f"rm *.pdf".split(" ")) 
        # p1 = subprocess.call(f"rm *.h5p".split(" ")) 
        print(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{filename}{file_extension}")))
        pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{filename}{file_extension}")))
        print(f"{filename}{file_extension}")
        dpi = request.form['dpi']
        res = request.form['resolution']
        print("Call Main Function --------------------------")
        p1 = subprocess.call(f"python3 generateh5p.py {filename}{file_extension}  --dpi {dpi} --resolution {res} --webOutput {uploads_dir}".split(" ")) 
        p1 = subprocess.call(f"mv {uploads_dir}/{filename}{file_extension}  {uploads_dir}/out{file_extension} ".split(" ")) 
        number = 1 ## Place Holder for the Render script 
        Global_H5pFileName = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"{filename}.h5p"))
        
    return render_template("index.html", prediction = number, file_name = Global_H5pFileName)


@app.route("/download", methods = ['GET', 'POST'])
def download():
    if request.method == 'POST':
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f"out.h5p")) , as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)
    