# importing the required libraries
import os
from flask import Flask, render_template, request
from jinja2 import Undefined
from werkzeug.utils import secure_filename
import shutil


# TODO: import the model from model.py
from model import * 

#  vars
_id = 0

# initialising the flask app
app = Flask(__name__)
# vars
# Creating the upload folder
upload_folder = "uploads/"

# delete uploads content on start
for f in os.listdir(upload_folder):
    shutil.rmtree(os.path.join(upload_folder, f))

if not os.path.exists(upload_folder):
   os.mkdir(upload_folder)

# Configuring the upload folder
app.config['UPLOAD_FOLDER'] = upload_folder
# configuring the allowed extensions
allowed_extensions = ['dcm', 'png']

def check_file_extension(filename):
    return filename.split('.')[-1] in allowed_extensions

# The path for uploading the file
@app.route('/')
def upload_file():
   return render_template('upload.html')

@app.route('/upload', methods = ['GET', 'POST'])
def uploadfile():
    global _id
    global patient_id
    patient_id = str(_id).zfill(5)
    _id = _id+1

    if request.method == 'POST': # check if the method is post
        files = request.files.getlist('files') # get the file from the files object
        # print(files)
        os.makedirs(f"./uploads/{patient_id}")
    for f in files:
        print(f.filename)
        # Saving the file in the required destination
        if check_file_extension(f.filename):
            f.save(os.path.join(f"./uploads/{patient_id}", secure_filename(f.filename))) # this will secure the file
    predict(patient_id)
    return 'file uploaded successfully' # Display this message after uploading
		

if __name__ == '__main__':
    app.run(debug=True) # running the flask app
