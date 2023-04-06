from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import json

import database.db_utils as db_utils
from logs import logger
from utils.exceptions import APIException


class GetFriends(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        db_utils.validate_user(user_id)
        friends = db_utils.get_friends(user_id=user_id)
        return Response(
            json.dumps(friends, indent=4),
            status=200
        )


class DeleteFriend(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        db_utils.validate_user(user_id)
        db_utils.delete_friendship(user_id_1=user_id, user_id_2=content['user_id'])
        return Response(
            status=200
        )
