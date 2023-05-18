from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import json

import services.authorization as auth_service
import services.friends as friends_service
from logs import logger
from utils.exceptions import APIException


class CreateFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        friends_service.create_friendship_request(sender_id=user_id, recipient_id=content['recipient_id'])
        return Response(
            status=200
        )


class DeleteFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        friends_service.delete_friendship_request(sender_id=user_id, recipient_id=content['recipient_id'])
        return Response(
            status=200
        )


class AcceptFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        friends_service.accept_friendship_request(sender_id=content['sender_id'], recipient_id=user_id)
        return Response(
            status=200
        )


class RejectFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        content = request.get_json(force=True)
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        friends_service.reject_friendship_request(sender_id=content['sender_id'], recipient_id=user_id)
        return Response(
            status=200
        )


class GetIncomingFriendshipRequests(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        requests = friends_service.get_incoming_friendship_requests(user_id=user_id)
        return Response(
            json.dumps(requests, indent=4),
            status=200
        )


class GetOutgoingFriendshipRequests(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        auth_service.validate_user(user_id)
        requests = friends_service.get_outgoing_friendship_requests(user_id=user_id)
        return Response(
            json.dumps(requests, indent=4),
            status=200
        )
