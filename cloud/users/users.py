from io import BytesIO
from flask import (Blueprint, render_template, url_for, request,
redirect, session, flash, send_file)
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from cloud.models import User, Audio, Document, Image, Video
from .forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from cloud import db
from cloud.config import Config

users = Blueprint('users', __name__, static_folder='static',
template_folder='templates')

# AUTHENTICATION:
@users.route('/create-account', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        name = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if name != None:
            flash("Username already exists!")
        elif email != None:
            flash("There's already an account associated with this email!")
        else:
            try:
                user = User(first_name=form.first_name.data, last_name=form.last_name.data, \
                    username=form.username.data, email=form.email.data)
                user.password = form.password.data
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=form.remember.data)
                return redirect(url_for('users.home'))
            except:
                return "<h1> :( Something Went Wrong!</h1>"
    return render_template('users/register.html', form=form, title="Create Account")

@users.route('/login', methods=['POST', 'GET'])
def login():
    ''' User login. '''
    # Checks if the user is still logged in
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('users.home')
        return redirect(next_page)
    return render_template('users/login.html', form=form, title="Login")


# PAGES
@users.route('/home', methods=['GET'])
@login_required
def home():
    ''' Home page '''
    user = User.query.filter_by(username=current_user.username).first()
    audios = user.audios.all()
    documents = user.documents.all()
    images = user.images.all()
    videos = user.videos.all()
    files = audios + documents + images + videos
    return render_template('users/home.html', audios=audios, documents=documents, images=images, videos=videos, files=files, title="Home")

    

def allowed_file(filename, file_type):
    ''' This checks if the file extension is allowed depending on the file type
        to be uploaded. '''
    if file_type == 'audio':
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.AUD_ALLOWED_EXTENSIONS
    elif file_type == 'document':
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.DOC_ALLOWED_EXTENSIONS
    elif file_type == 'image':
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.IMG_ALLOWED_EXTENSIONS
    else:
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in Config.VID_ALLOWED_EXTENSIONS
    
# FILE UPLOAD VIEWS:
@users.route('/upload-audio', methods=['POST', 'GET'])
@login_required
def upload_audio():
    ''' Upload audio files. '''
    file_type = 'audio'
    if request.method == 'POST':
        # Check if the post request has the file part.
        if 'file' not in request.files:
            flash('No file part!', 'error')
            return redirect(url_for('users.upload_audio'))
        audio = request.files['file']
        # Check if user selected the file or filename is not empty.
        if audio.filename == '':
            flash('Filename empty or file not selected!', 'error')
            return redirect(url_for('users.upload_audio'))
        # Check if file extension is allowed.
        if allowed_file(audio.filename, audio) == False:
            flash('File extension not allowed!', 'error')
            return redirect(url_for('users.upload_audio'))
        
        # If everything checks out
        if audio:
            filename = secure_filename(audio.filename)
            user = User.query.filter_by(username=current_user.username).first()
            aud =  Audio(name=filename, content=audio.read(), user=user)
            db.session.add(aud)
            db.session.commit()
            flash("File Uploaded", "success")
            return redirect(url_for('users.home'))
    return render_template('users/upload.html', file_type=file_type, title="Upload-Audio")

@users.route('/upload-document', methods=['POST', 'GET'])
@login_required
def upload_document():
    ''' Upload document files. '''
    file_type = 'document'
    if request.method == 'POST':
        # Check if the post request has the file part.
        if 'file' not in request.files:
            flash('No file part!', 'error')
            return redirect(url_for('users.upload_document'))
        
        document = request.files['file']
        # Check if user selected the file or filename is not empty.
        if document.filename == '':
            flash('Filename empty or file not selected!', 'error')
            return redirect(url_for('users.upload_document'))
        
        # Check if file extension is allowed.
        if allowed_file(document.filename, file_type) == False:
            flash('File extension not allowed!', 'error')
            return redirect(url_for('users.upload_document'))
        
        
        # If everything checks out
        if document:
            filename = secure_filename(document.filename)
            user = User.query.filter_by(username=current_user.username).first()
            doc =  Document(name=filename, content=document.read(), user=user)
            db.session.add(doc)
            db.session.commit()
            flash('File uploaded!', 'success')
            return redirect(url_for('users.home'))
    return render_template('users/upload.html', file_type=file_type, title="Upload-Document")

@users.route('/image-upload', methods=['POST', 'GET'])
@login_required
def upload_image():
    ''' Upload image files. '''
    file_type = 'image'
    if request.method == 'POST':
        # Check if the post request has the file part.
        if 'file' not in request.files:
            flash('No file part!', 'error')
            return redirect(url_for('users.upload_image'))
        
        image = request.files['file']
        # Check if user selected the file or filename is not empty.
        if image.filename == '':
            flash('Filename empty or file not selected!', 'error')
            return redirect(url_for('users.upload_image'))
        
        # Check if file extension is allowed.
        if allowed_file(image.filename, file_type) == False:
            flash('File extension not allowed!', 'error')
            return redirect(url_for('users.upload_image'))
        
        
        # If everything checks out
        if image:
            filename = secure_filename(image.filename)
            user = User.query.filter_by(username=current_user.username).first()
            img =  Image(name=filename, content=image.read(), user=user)
            db.session.add(img)
            db.session.commit()
            flash('File uploaded!', 'success')
            return redirect(url_for('users.home'))
    return render_template('users/upload.html', file_type=file_type, title="Upload-Image")

@users.route('/upload-video', methods=['POST', 'GET'])
@login_required
def upload_video():
    ''' Upload video files. '''
    file_type = 'video'
    if request.method == 'POST':
        # Check if the post request has the file part.
        if 'file' not in request.files:
            flash('No file part!', 'error')
            return redirect(url_for('users.upload_video'))
        
        
        video = request.files['file']
        # Check if user selected the file or filename is not empty.
        if video.filename == '':
            flash('Filename empty or file not selected!', 'error')
            return redirect(url_for('users.upload_video'))
        
        # Check if file extension is allowed.
        if allowed_file(video.filename, file_type) == False:
            flash('File extension not allowed!', 'error')
            return redirect(url_for('users.upload_video'))
        
        # If everything checks out
        if image:
            filename = secure_filename(image.filename)
            user = User.query.filter_by(username=current_user.username).first()
            vid =  Video(name=filename, content=file.read(), user=user)
            db.session.add(vid)
            db.session.commit()
            flash('File uploaded!', 'success')
            return redirect(url_for('users.home'))
    return render_template('users/upload.html', file_type=file_type, title="Upload-Video")


# FILE DOWNLOAD VIEWS:
@users.route('/<int:id>/download-audio')
@login_required
def download_audio(id):
    audio = Audio.query.get_or_404(id)
    return send_file(BytesIO(audio.content), attachment_filename=audio.audio_name, as_attachment=True)

@users.route('/<int:id>/download-document')
@login_required
def download_document(id):
    document = Document.query.get_or_404(id)
    return send_file(BytesIO(document.content), attachment_filename=document.document_name, as_attachment=True)

@users.route('/<int:id>/download-image')
@login_required
def download_image(id):
    image = Image.query.get_or_404(id)
    return send_file(BytesIO(image.content), attachment_filename=image.image_name, as_attachment=True)

@users.route('/<int:id>/download-video')
@login_required
def download_video(id):
    video = Video.query.get_or_404(id)
    return send_file(BytesIO(video.content), attachment_filename=video.video_name, as_attachment=True)


# FILE DELETION VIEWS:
@users.route("/<int:id>/delete-audio")
@login_required
def delete_audio(id):
    audio = Audio.query.get_or_404(id)
    db.session.delete(audio)
    db.session.commit()
    flash("File deleted!", 'danger')
    return redirect(url_for('users.home'))

@users.route("/<int:id>/delete-document")
@login_required
def delete_document(id):
    document = Document.query.get_or_404(id)
    db.session.delete(document)
    db.session.commit()
    flash("File deleted!", 'danger')
    return redirect(url_for('users.home'))

@users.route("/<int:id>/delete-image")
@login_required
def delete_image(id):
    image = Image.query.get_or_404(id)
    db.session.delete(image)
    db.session.commit()
    flash("File deleted!", 'danger')
    return redirect(url_for('users.home'))

@users.route("/<int:id>/delete-video")
@login_required
def delete_video(id):
    video = Video.query.get_or_404(id)
    db.session.delete(video)
    db.session.commit()
    flash("File deleted!", 'danger')
    return redirect(url_for('users.home'))

# LOGOUT:
@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# DELETE/REMOVE CLOUD ACCCOUNT:
@users.route('/delete-account')
@login_required
def delete_account():
    user = User.query.filter_by(username=current_user.username).first()
    audios = user.audios.all()
    documents = user.documents.all()
    images = user.images.all()
    videos = user.videos.all()

    if audios != None:
        for audio in audios:
            db.session.delete(audio)
        db.session.commit()
    
    if documents != None:
        for document in documents:
            db.session.delete(document)
        db.session.commit()

    if images != None:
        for image in images:
            db.session.delete(image)
        db.session.commit()
    
    if videos != None:
        for video in videos:
            db.session.delete(video)
        db.session.commit()

    db.session.delete(user)
    logout_user()
    db.session.commit()
    flash("Account was deleted successfully! Good riddance ...", 'danger')
    
    return redirect(url_for('index'))
