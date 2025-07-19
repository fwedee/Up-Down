from app.extensions import db
from sqlalchemy import DateTime
from datetime import datetime, timezone

class TextContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<TextContent {self.id}>'

class FileReference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_reference = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    file_extension = db.Column(db.String(10), nullable=False)
    created_at = db.Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<FileReference {self.filename}>'