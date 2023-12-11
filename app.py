from flask import Flask, render_template, request, make_response, url_for, send_from_directory
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import numpy as np
import os
import cv2

from azureproject import mongodb
from requests import RequestException

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if not 'WEBSITE_HOSTNAME' in os.environ:
   # local development, where we'll use environment variables
   print("Loading config.development.")
   app.config.from_object('azureproject.development')
else:
   # production
   print("Loading config.production.")
   app.config.from_object('azureproject.production')


@app.route('/', methods=['GET', 'POST'])
def index():

    restaurants_annotated = []       

    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
@csrf.exempt
def upload():
    imagefile = request.files.get('myfile', '').read()
    img = cv2.imdecode(np.fromstring(imagefile, np.uint8), cv2.IMREAD_COLOR)
    if request.form.get('select') == "grayscale" :
        img = toGray(img)
    else:
        img = cv2.flip(img, 0)
    retval, buffer = cv2.imencode('.png', img)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/png'
    return response

def toGray(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

if __name__ == '__main__':
   app.run()