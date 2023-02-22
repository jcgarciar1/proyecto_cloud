from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_celeryext import FlaskCeleryExt  # new
from back.utils import make_celery  # new

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
api = Api()
mail = Mail()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)  # new

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    try:
        app.config.from_pyfile('config.py')
    except:
        pass
    mail.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    ext_celery.init_app(app)  # new



    import back.models
    with app.app_context():
        db.create_all()

    import back.views
    import back.routes
    api.init_app(app)

    return app

def _endpoint_from_view_func(view_func):
    """Internal helper that returns the default endpoint for a given
    function.  This always is the function name.
    """
    assert view_func is not None, "expected view func if endpoint is not provided."
    return view_func.__name__
