from flask import Blueprint, request
from app.services.user_service import create_text_content, get_recent_texts

text_upload = Blueprint('text_upload', __name__)

@text_upload.route('', methods=['POST'])
def upload_text():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
       json = request.json
       text = json['text']
       database_text = create_text_content(text)

       return {
            "text" : database_text.content
       }
    return '404'
