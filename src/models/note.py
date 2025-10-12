from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, time
import json
from src.models.user import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # store tags as JSON string in text column for compatibility
    tags = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.Date, nullable=True)
    event_time = db.Column(db.Time, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.title}>'

    def get_tags(self):
        if not self.tags:
            return []
        try:
            return json.loads(self.tags)
        except Exception:
            # fallback: comma separated string
            return [t.strip() for t in (self.tags or '').split(',') if t.strip()]

    def set_tags(self, tags_list):
        try:
            if tags_list is None:
                self.tags = None
            else:
                # ensure it's a list
                if isinstance(tags_list, str):
                    tags_list = [t.strip() for t in tags_list.split(',') if t.strip()]
                self.tags = json.dumps(tags_list)
        except Exception:
            self.tags = None

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'tags': self.get_tags(),
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'event_time': self.event_time.isoformat() if self.event_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

