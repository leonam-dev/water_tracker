import re, pytz

from datetime import datetime
from app.models import User, WaterIntake
from marshmallow import Schema, fields, post_load, pre_load, validates, ValidationError, validates_schema


class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.Str(required=True)
    weight = fields.Float(required=True)
    daily_goal = fields.Float(dump_only=True)

    @pre_load
    def process_name(self, data, **kwargs):
        if 'name' in data:
            data['name'] = data['name'].strip()
            data['name'] = re.sub(" +", " ", data['name'])
        return data
    
    @validates('name')
    def validate_name(self, value):
        if len(value) < 3:
            raise ValidationError('Name must have at least 3 letters.')
        if not re.match("[A-Za-z ]+$", value):
            raise ValidationError('Name must contain only letters and spaces.')
        
    @validates('weight')
    def validate_weight(self, value):
        if value <= 0:
            raise ValidationError('Weight must be greater than zero.')
        
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class WaterIntakeBaseSchema(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.UUID(required=True)

    @post_load
    def make_user_intake(self, data, **kwargs):
        data['user_id'] = str(data['user_id'])

        if 'date' in data and isinstance(data['date'], str):
            data['date'] = datetime.strptime(data['date'], '%d-%m-%Y').date()

        return WaterIntake(**data)


class WaterIntakeAddSchema(WaterIntakeBaseSchema):
    amount = fields.Float(required=True)
    date = fields.DateTime(dump_only=True, format="%d-%m-%Y %H:%M:%S")

    @validates('amount')
    def validate_amout(self, value):
        if value <= 0:
            raise ValidationError('Amount must be greater than zero.')


class WaterIntakeRetrieverSchema(WaterIntakeBaseSchema):
    amount = fields.Float(required=False)
    date = fields.Str(required=False)

    @pre_load
    def process_date(self, data, **kwargs):
        if not data['date']:
            data['date'] = datetime.now(pytz.timezone('America/Sao_Paulo')).date().strftime('%d-%m-%Y')
        return data
    
    @validates('date')
    def validate_date(self, value):
        try:
            date = datetime.strptime(value, '%d-%m-%Y').date()
        except:
            raise ValidationError('Invalid date. The correct format is DD-MM-YYY.')
        
        today = datetime.now().date()
        if date > today:
            raise ValidationError('The date cannot be in the future.')
