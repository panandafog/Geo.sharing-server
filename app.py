from flask import Flask
from logs import logger
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from configuration.configurator import Configurator
from resources.routes import initialize_routes
from secrets import JWT_SECRET_KEY

app = Flask(__name__)

logger.init_logging()
configurator = Configurator()

app.config['MONGODB_SETTINGS'] = {
    'host': configurator.db_uri
}
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

initialize_db(app)


if __name__ == '__main__':
    initialize_routes(api)
    app.run(
        host='0.0.0.0',
        port=5566
    )
