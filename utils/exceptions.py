import json
from flask import Response

class APIException(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    @classmethod
    def from_exception(cls, exception):
        if isinstance(exception, cls):
            return exception
        print("ex:")
        print(str(exception))
        return cls(455, str(exception))

    def json_body(self):
        return json.dumps({'error': self.description})

    def flask_response(self):
        return Response(
            self.json_body(),
            status=self.code
        )
