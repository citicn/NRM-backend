from flask import Blueprint, send_from_directory, current_app

uploadsBp = Blueprint('uploads', __name__)


@uploadsBp.route('/uploads/<filename>', methods=["GET"])
def uploadedImg(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
