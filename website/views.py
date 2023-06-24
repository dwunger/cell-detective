from flask import Blueprint, render_template, Flask, request, redirect, url_for
import cv2  
from PIL import Image
import io
import base64
import numpy as np
import yolov5.detect



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
    
    for file in files:
        if file.filename == '':
            return 'No selected file'
            
        file_in_memory = file.read()
        image = Image.open(io.BytesIO(file_in_memory))

        # save image to a temporary file
        image_path = 'temp.jpg'
        image.save(image_path)

        # # call the detect.py script
        # command = ['python', 'C:/Users/dento/Desktop/Python_Projects/colab/image-segmentation/detect.py',
        #            '--weights', "C:/Users/dento/Desktop/Python_Projects/colab/image-segmentation/yolov5/runs/train/kb_counter9/weights/best.pt",
        #            '--img', '1500',
        #            '--conf', '0.4',
        #            '--source', image_path,
        #            '--line-thickness', '2',
        #            '--hide-labels']
        # subprocess.run(command, check=True)
        image = yolov5.detect.run(source=image_path, conf_thres = 0.4, line_thickness = 2, weights = r'C:/Users/dento/Desktop/Python_Projects/colab/image-segmentation/yolov5/runs/train/kb_counter9/weights/best.pt', exist_ok=True)
        # YOLOv5 saves processed images to 'runs/detect/exp' by default
        processed_image_path = os.path.join('runs', 'detect', 'exp', os.path.basename(image_path))

        # read the processed image
        processed_image = Image.open(processed_image_path)
        buf = io.BytesIO()
        processed_image.save(buf, format='JPEG')
        buf.seek(0)
        image_string = base64.b64encode(buf.read()).decode()
        image_strings.append(image_string)

        # remove the temporary and processed image files
        os.remove(image_path)
        os.remove(processed_image_path)

    # We are passing the list of base64 image strings to the template
    return render_template('upload.html', image_strings=image_strings)

    
    # We are passing the list of base64 image strings to the template
    return render_template('upload.html', image_strings=image_strings)

