from flask import Response, request
from flask_jwt_extended import create_access_token
import datetime

import database.db_utils as db_utils
from database.models import User
from flask_restful import Resource
from logs import logger
from utils.exceptions import APIException


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
            response = APIException.from_exception(e).flask_response()
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
            response = APIException.from_exception(e).flask_response()
        return response


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))

            logger.log(str(user.is_confirmed()))

            if not authorized:
                raise APIException(401, 'Email or password invalid')

            if not user.is_confirmed():
                raise APIException(402, 'Email is not confirmed')

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            response = {
                   'token': access_token,
                   'id': str(user.id),
                   'username': str(user.username),
                   'email': str(user.email)
            }, 200
        except Exception as e:
            logger.error(str(e))
            response = APIException.from_exception(e).flask_response()
        return response
