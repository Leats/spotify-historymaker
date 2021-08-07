import os

import configparser

from sqlalchemy.engine import URL

from flask import Flask


def create_app():
    config = configparser.ConfigParser()
    config.read(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "config.ini"))
    )
    if not config:
        raise ValueError("No valid config.ini available.")

    try:
        db_uri = URL.create(
            "postgresql",
            username=config["Database"]["user"],
            password=config["Database"]["password"],
            port=config["Database"]["port"],
            host=config["Database"]["host"],
            database=config["Database"]["dbname"],
        )
    except Exception as err:
        print(err)
        raise ValueError("Error in config.ini")

    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=db_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    from historymaker.models import db

    db.init_app(app)

    from historymaker.views import data
    from historymaker.views import visualizations

    app.register_blueprint(data.bp)
    app.register_blueprint(visualizations.bp)

    return app


app = create_app()
