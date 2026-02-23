from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required, login_user, logout_user

from models import User
from utils.extensions import db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"success": False, "error": "Email already registered"}), 409

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_user(user)
    return jsonify({"success": True, "user": {"id": user.id, "email": user.email}})


@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

    login_user(user)
    return jsonify({"success": True, "user": {"id": user.id, "email": user.email}})


@auth_bp.route("/api/auth/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"success": True})


@auth_bp.route("/api/auth/me", methods=["GET"])
def me():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False}), 200
    return jsonify({"authenticated": True, "user": {"id": current_user.id, "email": current_user.email}})
