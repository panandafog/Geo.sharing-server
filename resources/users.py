from flask import Response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

from database.models import User
import database.db_utils as db_utils
from logs import logger
import json
from utils.exceptions import APIException


class HelloApi(Resource):
    def get(self):
        return 'Hello World!'


class RequestPasswordChangeApi(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            db_utils.request_password_change(user_id)
            response = Response(
                status=200
            )
        except Exception as e:
            logger.exception()
            response = APIException.from_exception(e).flask_response()
        return response


class ChangePasswordApi(Resource):
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            db_utils.change_password(
                user_id=user_id,
                code=body.get('code'),
                new_password=body.get('new_password')
            )
            response = Response(
                status=200
            )
        except Exception as e:
            logger.exception()
            response = APIException.from_exception(e).flask_response()
        return response


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
            logger.exception()
            response = APIException.from_exception(e).flask_response()
        return response


class SearchUserApi(Resource):
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            db_utils.validate_user(user_id)
            content = request.get_json(force=True)
            users = db_utils.search_users(content['query'], user_id)
            response = Response(
                json.dumps(users, indent=4),
                status=200
            )
        except Exception as e:
            logger.exception()
            response = APIException.from_exception(e).flask_response()
        return response


class LocationSaveApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            user_id = get_jwt_identity()
            db_utils.validate_user(user_id)
            logger.log(str(content))
            db_utils.save_user_location(user_id=user_id, latitude=content['latitude'], longitude=content['longitude'])
            # database.update_geolocation(user_id=content['user_id'], latitude=content['latitude'], longitude=content['longitude'])
            response = Response(
                status=200
            )
        except Exception as e:
            logger.exception()
            response = APIException.from_exception(e).flask_response()
        return response


class ProfilePictureApi(Resource):
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            db_utils.validate_user(user_id)
            picture = request.files['picture']
            logger.log(str(picture))
            db_utils.save_profile_picture(user_id=user_id, picture=picture)
            response = Response(
                status=200
            )
        except Exception as e:
            logger.exception()
            response = APIException.from_exception(e).flask_response()
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
            logger.exception()
            response = APIException.from_exception(e).flask_response()
        return response
