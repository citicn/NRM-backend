import os
import uuid
import time
from flask import current_app
from werkzeug.utils import secure_filename
from ..config import Config

MAX_FILE_SIZE = 4 * 1024 * 1024
def allowedExt(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def saveImg(file):
        if file and allowedExt(file.filename):
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0)
            if file_length > MAX_FILE_SIZE:
                return {"error": "Velicina fajla je preko 4MB!"},401
            ext = file.filename.rsplit('.', 1)[1].lower()
            timestamp = int(time.time())
            random_name = f"{uuid.uuid4().hex}_{timestamp}.{ext}"
            filename = secure_filename(random_name)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            return filename
        return None
