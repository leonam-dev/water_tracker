from flask import request, jsonify
from app.api import bp
from app.api.schemas import UserSchema, WaterIntakeAddSchema, WaterIntakeRetrieverSchema
from app.services import UserService, WaterIntakeService
from http import HTTPStatus
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import InternalServerError, BadRequest, NotFound
from sqlalchemy.orm.exc import NoResultFound


user_schema = UserSchema()
intake_add_schema = WaterIntakeAddSchema()
intake_retriever_schema = WaterIntakeRetrieverSchema()


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


@bp.route('/users/<uuid:user_id>/intakes', methods=['POST'])
def add_intake(user_id):
    try:
        data = request.get_json() or {}
        data['user_id'] = user_id
        water_intake = intake_add_schema.load(data)
        intake = WaterIntakeService.add_intake(water_intake)
        return jsonify(intake_add_schema.dump(intake)), HTTPStatus.CREATED
    except ValidationError as err:
        raise BadRequest(err.messages)
    except NoResultFound as err:
        raise NotFound(str(err))
    except Exception as err:
        raise InternalServerError(str(err))


@bp.route('/users/<uuid:user_id>/intakes', methods=['GET'])
def get_intake(user_id):
    try:
        date = request.args.get('date')
        data = {'user_id': user_id, 'date': date}
        water_intake = intake_retriever_schema.load(data)
        intake = WaterIntakeService.get_intake_by_date(water_intake)
        return jsonify(intake), HTTPStatus.OK
    except ValidationError as err:
        raise BadRequest(err.messages)
    except NoResultFound as err:
        raise NotFound(str(err))
    except Exception as err:
        raise InternalServerError(str(err))


@bp.route('/users/<uuid:user_id>/intakes-history', methods=['GET'])
def intakes_history(user_id):
    try:
        intakes = WaterIntakeService.get_all_intake(user_id=str(user_id))
        return jsonify(intakes), HTTPStatus.OK
    except NoResultFound as err:
        raise NotFound(str(err))
    except Exception as err:
        raise InternalServerError(str(err))
