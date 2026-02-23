#!/usr/bin/env python3
"""
CareerGuideAI Web Application
App factory and route registration.
"""

import os

from dotenv import load_dotenv
from flask import Flask

from models import User
from routes.api import api_bp
from routes.auth import auth_bp
from routes.main import main_bp
from routes.roadmaps import roadmaps_bp
from utils.extensions import cache, db, limiter, login_manager


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/career_ai"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_URL"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    app.config["CACHE_DEFAULT_TIMEOUT"] = 3600
    app.config["CELERY_BROKER_URL"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    app.config["CELERY_RESULT_BACKEND"] = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    db.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(roadmaps_bp)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    return app


app = create_app()


if __name__ == "__main__":
    print("🚀 CareerGuideAI Web Application Starting...")
    print("📱 Available at: http://127.0.0.1:5001")
    print("🌐 Also try: http://localhost:5001")
    print("🌐 Network access: http://10.58.30.179:5001")
    app.run(debug=True, host="0.0.0.0", port=5001)
