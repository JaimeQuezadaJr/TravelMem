from flask import Flask
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")  

# logging.basicConfig(filename='record.log', level=logging.ERROR)

UPLOAD_FOLDER = '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 