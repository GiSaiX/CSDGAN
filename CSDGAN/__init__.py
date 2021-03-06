import CSDGAN.utils.constants as cs
from config import Config
from flask import Flask
from redis import Redis
import rq
from flask_moment import Moment
import os

moment = Moment()


def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('CSDGAN', connection=app.redis)
    moment.init_app(app)

    os.makedirs(app.instance_path, exist_ok=True)

    try:
        os.makedirs(cs.LOG_FOLDER, exist_ok=True)
        os.makedirs(cs.RUN_FOLDER, exist_ok=True)
        os.makedirs(cs.OUTPUT_FOLDER, exist_ok=True)
        os.makedirs(cs.UPLOAD_FOLDER, exist_ok=True)
    except PermissionError:
        raise NameError('Please change DOCKERIZED to False in .env')

    from CSDGAN.utils import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import about
    app.register_blueprint(about.bp)

    from . import create
    app.register_blueprint(create.bp)

    from . import viz
    app.register_blueprint(viz.bp)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    return app



