import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    FLASK_APP = os.environ.get('FLASK_APP')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'database.db')
    FLASK_ENV = development
    AUD_ALLOWED_EXTENSIONS = {'mp3', 'm4a', 'flac', 'wav', 'wma'}
    DOC_ALLOWED_EXTENSIONS = {'doc', 'docx', 'odt', 'pdf', 'xls', 'xlsx',\
        'ods', 'ppt', 'pptx', 'txt'}
    IMG_ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'tiff', 'gif', 'psd', \
        'eps', 'ai', 'indd', 'raw'}
    VID_ALLOWED_EXTENSIONS = {'mp4', '3pg', 'ogg', 'wmv', 'webm', 'flv', 'wav'}
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True