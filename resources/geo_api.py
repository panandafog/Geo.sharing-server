import flask_restful

from utils.exceptions import APIException
from logs import logger

class GeoApi(flask_restful.Api):
    def handle_error(self, e):
        logger.exception()
        return APIException.from_exception(e).flask_response()