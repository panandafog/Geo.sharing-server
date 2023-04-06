import json
import jwt.exceptions
from flask import Response

unauthorized_code = 401

class APIException(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    @classmethod
    def from_exception(cls, exception):
        if isinstance(exception, cls):
            return exception
        if isinstance(exception, jwt.exceptions.ExpiredSignatureError):
            return cls(unauthorized_code, "Session expired")
        if isinstance(exception, jwt.exceptions.InvalidSignatureError):
            return cls(unauthorized_code, "Invalid signature")
        if isinstance(exception, jwt.exceptions.InvalidTokenError):
            return cls(unauthorized_code, "Invalid token")
        return cls(455, str(exception))

    def json_body(self):
        return json.dumps({'error': self.description})

    def flask_response(self):
        return Response(
            self.json_body(),
            status=self.code
        )
