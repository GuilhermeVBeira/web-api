import uuid

from sqlalchemy.dialects.postgresql import UUID

from web_app.main import db


class Client(db.Model):
    __tablename__ = "clients_client"

    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), index=True, nullable=False)
