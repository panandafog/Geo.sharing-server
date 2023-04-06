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
    def post(self):
        content = request.get_json(force=True)
        db_utils.request_password_change(email=content.get('email'))
        return Response(
            status=200
        )


class ChangePasswordApi(Resource):
    def post(self):
        content = request.get_json(force=True)
        body = request.get_json()
        db_utils.change_password(
            email=content.get('email'),
            code=body.get('code'),
            new_password=body.get('new_password')
        )
        return Response(
            status=200
        )


class SaveGeoApi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        logger.log(str(content))
        return Response(
            status=200
        )


class SearchUserApi(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        db_utils.validate_user(user_id)
        content = request.get_json(force=True)
        users = db_utils.search_users(content['query'], user_id)
        return Response(
            json.dumps(users, indent=4),
            status=200
        )


class LocationSaveApi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        db_utils.validate_user(user_id)
        logger.log(str(content))
        db_utils.save_user_location(user_id=user_id, latitude=content['latitude'], longitude=content['longitude'])
        return Response(
            status=200
        )


class ProfilePictureApi(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        db_utils.validate_user(user_id)
        picture = request.files['picture']
        logger.log(str(picture))
        db_utils.save_profile_picture(user_id=user_id, picture=picture)
        return Response(
            status=200
        )

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, location='args')
        user_id = parser.parse_args()['user_id']

        picture = db_utils.get_profile_picture(user_id)
        response = Response(
            picture,
            status=200
        )
        response.headers.set('Content-Type', 'image/jpeg')
        return response
