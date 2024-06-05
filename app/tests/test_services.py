import pytest
from app.models import User
from app.services import UserService
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
