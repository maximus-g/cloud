import os, pymysql
class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = 'this-is-a-secret-and-it-is-hard-to-guess-l-o-l'
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'database.db')
    MAX_CONTENT_LENGTH = 1024 * 1024
    AUD_ALLOWED_EXTENSIONS = {'mp3', 'm4a', 'flac', 'wav', 'wma'}
    DOC_ALLOWED_EXTENSIONS = {'doc', 'docx', 'odt', 'pdf', 'xls', 'xlsx',\
        'ods', 'ppt', 'pptx', 'txt'}
    IMG_ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg', 'tiff', 'gif', 'psd', \
        'eps', 'ai', 'indd', 'raw'}
    VID_ALLOWED_EXTENSIONS = {'mp4', '3pg', 'ogg', 'wmv', 'webm', 'flv', 'wav'}
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    SQLALCHEMY_TRACK_MODIFICATIONS=True