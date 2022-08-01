from flask import Flask
app = Flask(__name__)

import os
app.secret_key = os.environ.get("FLASK_SECRET_KEY")  

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 