import pytest, pytz

from datetime import datetime
from app.models import User, WaterIntake
from app.services import UserService, WaterIntakeService
from sqlalchemy.orm.exc import NoResultFound


def test_create_user(app):
    with app.app_context():
        user = User(name='Leonam Raone', weight=70)
        user = UserService.create_user(user)
        assert user.id is not None
        assert user.name == 'Leonam Raone'
        assert user.weight == 70
        assert user.daily_goal == 2450


def test_get_user(app, test_user):
    with app.app_context():
        user = UserService.get_user(test_user.id)
        assert user.id == test_user.id
        assert user.name == test_user.name
        assert user.weight == test_user.weight


def test_get_user_not_found(app):
    with app.app_context():
        with pytest.raises(NoResultFound):
            UserService.get_user(123)


def test_add_intake(app, test_user):
    with app.app_context():
        water_intake = WaterIntake(user_id=test_user.id, amount=500)
        intake = WaterIntakeService.add_intake(water_intake)
        assert intake.id is not None
        assert intake.user_id == test_user.id
        assert intake.amount == 500


def test_get_intake_by_date(app, test_user):
    with app.app_context():
        water_intake = WaterIntake(user_id=test_user.id, amount=500)
        WaterIntakeService.add_intake(water_intake)
        water_intake.date = datetime.now(pytz.timezone('America/Sao_Paulo')).date()
        intake = WaterIntakeService.get_intake_by_date(water_intake)
        assert intake['total_intake'] == 500
        assert intake['remaining'] == 1950


def test_get_all_intake(app, test_user):
    with app.app_context():
        water_intake1 = WaterIntake(user_id=test_user.id, amount=500)
        water_intake2 = WaterIntake(user_id=test_user.id, amount=1000)
        WaterIntakeService.add_intake(water_intake1)
        WaterIntakeService.add_intake(water_intake2)
        intakes = WaterIntakeService.get_all_intake(user_id=test_user.id)
        assert len(intakes) == 1
        assert intakes[0]['total_intake'] == 1500
        assert intakes[0]['remaining'] == 950
