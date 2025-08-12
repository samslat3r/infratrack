from datetime import datetime, timezone
from . import db 

### NYI: model relationships with cascading deletes ( + DB 'ON DELETE CASCADE' )


def tags_to_list(tag_string):
    return [t.strip() for t in tag_string.split(',') if t.strip()]

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    os = db.Column(db.String(64))
    tags = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def tag_list(self):
        return tags_to_list(self.tags or '')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    performed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    host = db.relationship('Host', backref=db.backref('tasks', lazy=True))

class Change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    changed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    host = db.relationship('Host', backref=db.backref('changes', lazy=True))
    