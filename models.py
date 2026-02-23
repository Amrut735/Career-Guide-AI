from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from utils.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    roadmaps = db.relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Roadmap(db.Model):
    __tablename__ = "roadmaps"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    guidance_text = db.Column(db.Text, nullable=True)
    results_json = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="roadmaps")
    items = db.relationship("RoadmapItem", back_populates="roadmap", cascade="all, delete-orphan")


class RoadmapItem(db.Model):
    __tablename__ = "roadmap_items"

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey("roadmaps.id"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    phase = db.Column(db.String(80), nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    roadmap = db.relationship("Roadmap", back_populates="items")
