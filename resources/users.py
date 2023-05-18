from flask import Response, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import json


import services.authorization as auth_service
import services.users as users_service
import services.pictures as pictures_service
from logs import logger


class RequestPasswordChangeApi(Resource):
    def post(self):
        content = request.get_json(force=True)
        auth_service.request_password_change(email=content.get('email'))
        return Response(
            status=200
        )


class ChangePasswordApi(Resource):
    def post(self):
        content = request.get_json(force=True)
        body = request.get_json()
        auth_service.change_password(
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
        auth_service.validate_user(user_id)
        content = request.get_json(force=True)
        users = users_service.search_users(content['query'], user_id)
        return Response(
            json.dumps(users, indent=4),
            status=200
        )


class LocationSaveApi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        logger.log(str(content))
        users_service.save_user_location(user_id=user_id, latitude=content['latitude'], longitude=content['longitude'])
        return Response(
            status=200
        )


class ProfilePictureApi(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        picture = request.files['picture']
        logger.log(str(picture))
        pictures_service.save_profile_picture(user_id=user_id, picture=picture)
        return Response(
            status=200
        )

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=str, location='args')
        user_id = parser.parse_args()['user_id']

        picture = pictures_service.get_profile_picture(user_id)
        response = Response(
            picture,
            status=200
        )
        response.headers.set('Content-Type', 'image/jpeg')
        return response

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        pictures_service.delete_profile_picture(user_id)

        response = Response(
            status=200
        )
        return response
