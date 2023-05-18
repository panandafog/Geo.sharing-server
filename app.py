import os
from flask import Flask
from logs import logger
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

import configuration.configurator as configuration
from database.db import initialize_db
from configuration.configurator import Configurator
from resources.routes import initialize_routes
from resources.geo_api import GeoApi
from secrets import JWT_SECRET_KEY

configuration.set_testing(False)

def create_app(configurator=None):
    if configurator is None:
        configurator = Configurator()

    app = Flask(__name__)

    app.config['MONGODB_SETTINGS'] = {
        'host': configurator.db_uri
    }
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["PROPAGATE_EXCEPTIONS"] = True

    api = GeoApi(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    initialize_db(app)
    initialize_routes(api)

    return app

def run():
    logger.init_logging()

    app = create_app()

    app.run(
        host='0.0.0.0',
        port=5566
    )


if __name__ == '__main__':
    run()
