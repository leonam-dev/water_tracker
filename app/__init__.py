from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from app.config import DevelopmentConfig


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
