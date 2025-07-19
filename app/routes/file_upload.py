import os
from flask import Blueprint, request, current_app, abort, send_from_directory, send_file
from werkzeug.utils import secure_filename, safe_join
from werkzeug.exceptions import RequestEntityTooLarge
from app.services.user_service import create_file_reference
from app.extensions import socketio
from app.models.models import FileReference

file_upload = Blueprint('file_upload', __name__)

@file_upload.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400

    for uploaded_file in request.files.getlist('file'):
        if uploaded_file.filename != '' and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            try:
                uploaded_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                extension = os.path.splitext(filename)[1].lower()
                file_ref = create_file_reference(
                    file_reference=os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
                    filename=os.path.splitext(filename)[0],
                    file_extension=extension[1:])

                socketio.emit('files_update', {
                    'files': [{
                        'name': f"{file_ref.filename}.{file_ref.file_extension}",
                        'url': f"/download/{file_ref.id}",
                        'uploaded': file_ref.created_at.isoformat()
                    }]
                })

            except Exception as e:
                return f'Error saving file: {str(e)}', 500
        else:
            return 'This filetype is not supported by the application', 400

    return '', 204

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@file_upload.errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    return 'File is too large', 413


@file_upload.route('/download/<int:file_id>')
def download_file(file_id):
    file_ref = FileReference.query.get_or_404(file_id)
    absolute_path = os.path.abspath(file_ref.file_reference)

    directory, filename = os.path.split(file_ref.file_reference)

    if not os.path.exists(file_ref.file_reference):
        abort(404, description="File not found on server")

    print(f"DB Path: {file_ref.file_reference}")
    print(f"Exists: {os.path.exists(file_ref.file_reference)}")
    print(f"Absolute Path: {os.path.abspath(file_ref.file_reference)}")
    print(f"Readable: {os.access(file_ref.file_reference, os.R_OK)}")
    print(f"CWD: {os.getcwd()}")

    return send_file(
        absolute_path,
        as_attachment=True,
        download_name=f"{file_ref.filename}.{file_ref.file_extension}"
    )
