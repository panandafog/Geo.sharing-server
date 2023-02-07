from flask import Response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from database.models import User
import database.db_utils as db_utils
from logs import logger
import json


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


class SearchUserApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            users = db_utils.search_users(content['query'])
            response = Response(
                json.dumps(users, indent=4),
                status=200
            )
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


class ProfilePictureApi(Resource):
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            picture = request.files['picture']
            logger.log(str(picture))
            db_utils.save_profile_picture(user_id=user_id, picture=picture)
            response = Response(
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response

    @jwt_required()
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user_id', type=str, location='args')
            user_id = parser.parse_args()['user_id']

            picture = db_utils.get_profile_picture(user_id)
            response = Response(
                picture,
                status=200
            )
            response.headers.set('Content-Type', 'image/jpeg')
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response
