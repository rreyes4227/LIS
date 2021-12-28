import os
from flask import Flask
from flask_migrate import Migrate

# from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost:5432/lis',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from .api import analyzers, departments, lab_tests, orders, patients
    app.register_blueprint(analyzers.bp)
    app.register_blueprint(departments.bp)
    app.register_blueprint(lab_tests.bp)
    app.register_blueprint(orders.bp)
    app.register_blueprint(patients.bp)

    return app
