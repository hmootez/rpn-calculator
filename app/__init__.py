from flask import Flask

from flasgger import Swagger
# Import for Migrations
from flask_migrate import Migrate

from app.config import Config, DevelopmentConfig
from app.models import db


def create_app(conf=None):
    app = Flask(__name__)
    if conf:
        print(conf)
        app.config.from_object(conf)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    Migrate(app, db)
    Swagger(app)
    # Import routing to render the pages
    with app.app_context():
        from . import views
        db.create_all()
    return app





