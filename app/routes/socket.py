from app.extensions import socketio
from flask import request
from app.services.user_service import get_recent_files, get_recent_texts

@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected:{request.sid}')

@socketio.on('get_files')
def send_files():
    files = get_recent_files()
    print(files)
    socketio.emit('files_update',{
        'files': [{
          'name': f"{f.filename}.{f.file_extension}",
          'url': f"/download/{f.id}",
          'uploaded': f.created_at.isoformat()
        } for f in files]
    })

@socketio.on('get_texts')
def send_text():
    texts = get_recent_texts()
    print(texts)
    socketio.emit('texts_update',{
        'texts': [{
            'content': f"{text.content}"
        } for text in texts]
    })