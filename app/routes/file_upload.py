import os
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from app.services.user_service import create_file_reference, get_recent_files

file_upload = Blueprint('file_upload', __name__)

@file_upload.route('', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            try:
                uploaded_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                extension = os.path.splitext(filename)[1].lower()
                new_file = create_file_reference(
                    file_reference=os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
                    filename=os.path.splitext(filename)[0],
                    file_extension=extension[1:])
            except Exception as e:
                return f'Error saving file: {str(e)}', 500
        else:
            return 'This filetype is not supported by the application', 400

    return '', 204

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

# @upload_file.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'], name)

@file_upload.errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    return 'File is too large', 413
