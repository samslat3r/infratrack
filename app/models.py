from datetime import datetime, timezone
from . import db

def tags_to_list(tag_string: str):
    return [t.strip() for t in (tag_string or "").split(",") if t.strip()]


class Host(db.Model):
    __tablename__ = "host"

    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(64), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    os = db.Column(db.String(64))
    tags = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # ORM cascade + DB cascade
    tasks = db.relationship(
        "Task",
        backref="host",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy=True,
    )
    changes = db.relationship(
        "Change",
        backref="host",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy=True,
    )

    def tag_list(self):
        return tags_to_list(self.tags)


class Task(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(
        db.Integer,
        db.ForeignKey("host.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    description = db.Column(db.String(255), nullable=False)
    performed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class Change(db.Model):
    __tablename__ = "change"

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(
        db.Integer,
        db.ForeignKey("host.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    summary = db.Column(db.String(255), nullable=False)
    changed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
