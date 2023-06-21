from flask import Blueprint, render_template, Flask, request, redirect, url_for
import cv2  
from PIL import Image
import io
import base64
import numpy as np
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

@views.route('/upload', methods=['POST'])
def upload_file():
    if 'image_uploads' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('image_uploads')
    
    image_strings = []
    #!TODO:
    #!fetal_cells, maternal_cells = 0,0
    for file in files:
        if file.filename == '':
            return 'No selected file'
            # Read file into memory
        file_in_memory = file.read()
        
        # Convert file in memory to an image (assuming the file is an image)
        image = Image.open(io.BytesIO(file_in_memory))

        # Convert the image to grayscale using OpenCV
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        
        # Convert back to PIL Image
        gray_image_pil = Image.fromarray(gray_image)
        
        # Create a BytesIO object and save the grayscale image in it
        buf = io.BytesIO()
        gray_image_pil.save(buf, format='JPEG')
        buf.seek(0)
        
        # Convert binary data to base64 string
        image_string = base64.b64encode(buf.read()).decode()

        # assuming image_string is the base64 string of the processed image
        image_strings.append(image_string)
        
        #!TODO: 
        #!fetal, maternal = count_cells(image)
        #!fetal_cells += fetal
        #!maternal_cells += maternal
        #!TODO: add coordinates too and draw crosses on counted cells
    
    # We are passing the list of base64 image strings to the template
    return render_template('upload.html', image_strings=image_strings)

