from flask import Response, request
from flask_jwt_extended import create_access_token
import datetime

import database.db_utils as db_utils
from database.models import User
from flask_restful import Resource
from logs import logger


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            uid = db_utils.signup(
                username=body.get('username'),
                password=body.get('password'),
                email=body.get('email')
            )
            return {'id': str(uid)}, 200
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response

class ConfirmEmailApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            uid = db_utils.confirm_email(
                user_id=body.get('user_id'),
                code=body.get('code')
            )
            return {'id': str(uid)}, 200
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))

        logger.log(str(user.is_confirmed()))

        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        if not user.is_confirmed():
            return {'error': 'Email is not confirmed'}, 402

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'token': access_token, 'id': str(user.id)}, 200