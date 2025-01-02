from flask import jsonify


class HttpStatus:
    OK = 200
    CREATED = 201
    NOT_FOUND = 404
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500


class Docs:
    def __init__(self, title, description, example_response):
        self.title = title
        self.description = description
        self.example_response = example_response


class ErrResponse:
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        self.success = False

    @property
    def response(self):
        return jsonify({"error": self.error, "success": self.success}), self.status_code


class SuccessResponse:
    def __init__(self, message, data, status_code):
        self.data = data
        self.message = message
        self.success = True
        self.status_code = status_code

    @property
    def response(self):
        return (
            jsonify(
                {"data": self.data, "message": self.message, "success": self.success}
            ),
            self.status_code,
        )
