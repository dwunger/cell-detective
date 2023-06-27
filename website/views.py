from flask import Blueprint, render_template, Flask, request, redirect, url_for
import cv2  
from PIL import Image
import io
import base64
import numpy as np
# import importlib
import yolov5.detect
# importlib.reload(yolov5.detect)

def pprint(_str):
    _str = str(_str)
    import sys
    module = str(sys.modules[__name__])
    module = module.split('\\')[-1]
    module = module.replace("\'>", '')
    print('\n\n\n****\n'f"from: {module}.\n"+_str+'\n****\n\n\n')    

Image.MAX_IMAGE_PIXELS = 5000000000 
views = Blueprint("views", __name__)
app = Flask(__name__)

@views.route("/home")
@views.route("/")
def home():
    return render_template('home.html')

@views.route("/about")
def about():
    return render_template('about.html')

import subprocess
import shutil
import os

@views.route('/upload', methods=['POST'])
def upload_file():
    if 'image_uploads' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('image_uploads')
    image_strings = []
    
    for idx, file in enumerate(files):
        if file.filename == '':
            return 'No selected file'
        pprint(file.filename) 
        file_in_memory = file.read()
        image = Image.open(io.BytesIO(file_in_memory))
        if image.format == 'PNG':
            image = image.convert('RGB')
        # save image to a temporary file
        image_path = str(file.filename)
        image.save(image_path)
        if idx == 0:
            idx = ''
        image = yolov5.detect.run(source=image_path, 
                                  imgsz=(3000,3000),
                                  line_thickness = 1, 
                                  weights = '.\\yolov5\\runs\\train\\kb_counter10\\weights\\bestv15.pt', 
                                  exist_ok=True, 
                                  hide_labels=True,
                                  conf_only = True, 
                                  filename = str(file.filename), 
                                  box_to_point=True,
                                  save_txt = False)
        # YOLOv5 saves processed images to 'runs/detect/exp' by default
        
        processed_image_path = os.path.join('yolov5', 'runs', 'detect', 'exp', os.path.basename(image_path))
        processed_image_path = os.getcwd() + "\\" + processed_image_path

        # read the processed image
        processed_image = Image.open(processed_image_path)
        buf = io.BytesIO()
        processed_image.save(buf, format='JPEG')
        buf.seek(0)
        image_string = base64.b64encode(buf.read()).decode()
        image_strings.append(image_string)

        # remove the temporary and processed image files
        # os.remove(image_path)
        # os.remove(processed_image_path)

    # We are passing the list of base64 image strings to the template
    return render_template('upload.html', image_strings=image_strings)