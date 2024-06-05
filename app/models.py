import uuid, pytz

from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    daily_goal = db.Column(db.Float, nullable=False)

    def __init__(self, name, weight):
        self.id = str(uuid.uuid4())
        self.name = name
        self.weight = weight
        self.daily_goal = weight * 35 if weight is not None else 0

    intakes = db.relationship('WaterIntake', backref='user', lazy=True)


class WaterIntake(db.Model):
    __tablename__ = 'water_intakes'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')), nullable=False)
