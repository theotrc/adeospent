import os
from dotenv import load_dotenv
load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get('GCP')
# SECRET_KEY = os.environ.get('SECRET')
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = os.environ.get('FOLDER_PATH')