from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from bson import ObjectId
import os
import uuid

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
def upload():
    imagefile = request.files.get('myfile', '')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
   app.run()