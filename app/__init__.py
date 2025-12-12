from flask import Flask
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload folder exists
    import os

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    from app import routes

    app.register_blueprint(routes.bp)

    return app
