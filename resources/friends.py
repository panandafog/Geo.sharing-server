from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import json

import services.authorization as auth_service
import services.friends as friends_service


class GetFriends(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        friends = friends_service.get_friends(user_id=user_id)
        return Response(
            json.dumps(friends, indent=4),
            status=200
        )


class DeleteFriend(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        friends_service.delete_friendship(user_id_1=user_id, user_id_2=content['user_id'])
        return Response(
            status=200
        )
