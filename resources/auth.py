from flask import Response, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
import mongoengine.errors

import services.authorization as auth_service
from database.models import User
from flask_restful import Resource
from logs import logger
from utils.exceptions import APIException


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        uid = auth_service.signup(
            username=body.get('username'),
            password=body.get('password'),
            email=body.get('email')
        )
        return {'id': str(uid)}, 200


class ConfirmEmailApi(Resource):
    def post(self):
        body = request.get_json()
        uid = auth_service.confirm_email(
            user_id=body.get('user_id'),
            code=body.get('code')
        )
        return {'id': str(uid)}, 200


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        try:
            user = User.objects.get(email=body.get('email'))
        except mongoengine.errors.DoesNotExist:
            raise APIException(403, 'User not found')

        authorized = user.check_password(body.get('password'))

        if not authorized:
            raise APIException(403, 'Password is incorrect')

        if not user.is_confirmed():
            raise APIException(403, 'Email is not confirmed')

        expires = datetime.timedelta(days=180)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)

        return {
            'token': access_token,
            'id': str(user.id),
            'username': str(user.username),
            'email': str(user.email)
        }, 200


class DeleteUserApi(Resource):
    @jwt_required()
    def delete(self):
        print()
        user_id = get_jwt_identity()
        auth_service.delete_user(user_id)
        logger.log(user_id)
        return {'id': str(user_id)}, 200


class RefreshTokenApi(Resource):
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        return {
            'token': access_token,
            'id': str(user_id)
        }, 200
