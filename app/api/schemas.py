import re

from app.models import User
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

