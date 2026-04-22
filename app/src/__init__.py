from flask import Flask
from models import db
from config import Config
from routes import health_bp, task_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(task_bp)

    with app.app_context():
        db.create_all()

    return app