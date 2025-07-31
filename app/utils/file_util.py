import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
from ..config import Config

def allowedExt(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def saveImg(file):
    if file and allowedExt(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        random_name = f"{uuid.uuid4().hex}.{ext}"
        filename = secure_filename(random_name)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        return filename
    return None
