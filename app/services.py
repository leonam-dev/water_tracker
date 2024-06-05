from app import db
from app.models import User
from sqlalchemy.orm.exc import NoResultFound


class UserService:
    def create_user(user: User):
        name = user.name
        weight = user.weight
        user = User(name=name, weight=weight)
        db.session.add(user)
        db.session.commit()
        return user
    
    def get_user(user_id):
        user = db.session.get(User, str(user_id))
        if user is None:
            raise NoResultFound('User not found.')
        return user
    
