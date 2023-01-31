from flask import Response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import json

import database.db_utils as db_utils
from logs import logger
from utils.json import fix_array


class CreateFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            user_id = get_jwt_identity()
            db_utils.create_friendship_request(sender_id=user_id, recipient_id=content['recipient_id'])
            response = Response(
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response


class DeleteFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            user_id = get_jwt_identity()
            db_utils.delete_friendship_request(sender_id=user_id, recipient_id=content['recipient_id'])
            response = Response(
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response


class AcceptFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            user_id = get_jwt_identity()
            db_utils.accept_friendship_request(sender_id=content['sender_id'], recipient_id=user_id)
            response = Response(
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response


class RejectFriendshipRequestApi(Resource):
    @jwt_required()
    def post(self):
        try:
            content = request.get_json(force=True)
            user_id = get_jwt_identity()
            db_utils.reject_friendship_request(sender_id=content['sender_id'], recipient_id=user_id)
            response = Response(
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response


class GetIncomingFriendshipRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            requests = db_utils.get_incoming_friendship_requests(user_id=user_id)
            response = Response(
                json.dumps(requests, indent=4),
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response


class GetOutgoingFriendshipRequests(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            requests = db_utils.get_outgoing_friendship_requests(user_id=user_id)
            response = Response(
                json.dumps(requests, indent=4),
                status=200
            )
        except Exception as e:
            logger.error(str(e))
            response = Response(
                status=400
            )
        return response
