from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from database.models import User
import database.db_utils as db_utils
from logs import logger

class HelloApi(Resource):
    def get(self):
        return 'Hello World!'

class SaveGeoApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            logger.log(str(content))
            response = Response(
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response

class UserRegisterApi(Resource):
    def post(self):
        try:
            content = request.get_json(force=True)
            logger.log(str(content))
            # database.create_user(content)
            user = User(**content).save()
            id = user.id

            response = {'id': str(id)}, 200
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response

class LocationSaveApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            user_id = get_jwt_identity()
            logger.log(str(content))
            db_utils.save_user_location(user_id=user_id, latitude=content['latitude'], longitude=content['longitude'])
            # database.update_geolocation(user_id=content['user_id'], latitude=content['latitude'], longitude=content['longitude'])
            response = Response(
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response
