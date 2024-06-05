from flask import jsonify
from http import HTTPStatus
from app.api import bp
from marshmallow.exceptions import ValidationError


def error_response(status_code, message=None):
    payload = {'error': HTTPStatus(status_code).phrase}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response


@bp.app_errorhandler(ValidationError)
def handle_validation_error(error):
    return error_response(HTTPStatus.BAD_REQUEST, message=error.messages)


@bp.app_errorhandler(HTTPStatus.BAD_REQUEST)
def bad_request(error):
    return error_response(HTTPStatus.BAD_REQUEST, message=error.description)


@bp.app_errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error):
    return error_response(HTTPStatus.NOT_FOUND, message=error.description)


@bp.app_errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    return error_response(HTTPStatus.INTERNAL_SERVER_ERROR, message=error.description)
