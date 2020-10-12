import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from web_app.main import db


class FavoriteProduct(db.Model):
    __tablename__ = "clients_favorite_product"

    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    external_id = db.Column(UUID(), default=uuid.uuid4)
    client_id = db.Column(UUID(), db.ForeignKey("clients_client.id"))
    client = relationship("Client")


class Client(db.Model):
    __tablename__ = "clients_client"

    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(64), index=True, nullable=False)
    favorite_products = relationship(FavoriteProduct, backref="clients")
