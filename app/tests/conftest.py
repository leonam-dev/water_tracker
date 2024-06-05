import pytest
from app import create_app, db
from app.config import TestingConfig


@pytest.fixture(scope='function')
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def test_user(app):
    from app.models import User

    with app.app_context():
        user = User(name='Leonam Raone', weight=70)
        db.session.add(user)
        db.session.commit()
        yield user
