from flask import request, jsonify
from app.api import bp
from app.api.schemas import UserSchema
from app.services import UserService
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import InternalServerError, BadRequest, NotFound


user_schema = UserSchema()


@bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json() or {}
        user = user_schema.load(data)
        user = UserService.create_user(user)
        return jsonify(user_schema.dump(user)), HTTPStatus.CREATED
    except ValidationError as err:
        raise BadRequest(err.messages)
    except Exception as err:
        raise InternalServerError(str(err))

