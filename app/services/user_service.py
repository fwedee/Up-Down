from app.models.models import TextContent, FileReference
from app.extensions import db
from datetime import datetime

def create_text_content(content):
    new_text = TextContent(content=content)
    db.session.add(new_text)
    db.session.commit()
    return new_text

def create_file_reference(file_reference, filename, file_extension):
    new_file = FileReference(
        file_reference=file_reference,
        filename=filename,
        file_extension=file_extension
    )
    db.session.add(new_file)
    db.session.commit()
    return new_file

def get_recent_files(limit=5):
    return FileReference.query.order_by(FileReference.created_at.desc()).limit(limit).all()

def get_recent_texts(limit=3):
    return TextContent.query.order_by(TextContent.created_at.desc()).limit(limit).all()