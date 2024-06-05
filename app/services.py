import pytz

from app import db
from app.models import User, WaterIntake
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime


class UserService:
    @staticmethod
    def create_user(user: User):
        name = user.name
        weight = user.weight
        user = User(name=name, weight=weight)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user(user_id):
        user = db.session.get(User, str(user_id))
        if user is None:
            raise NoResultFound('User not found.')
        return user
    

class WaterIntakeService:
    @staticmethod
    def add_intake(water_intake: WaterIntake):
        UserService.get_user(water_intake.user_id)
        db.session.add(water_intake)
        db.session.commit()
        return water_intake

    @staticmethod
    def _calculate_intake_summary(user, intakes):
        total_intake = sum(intake.amount for intake in intakes)
        remaining = max(user.daily_goal - total_intake, 0)
        percentage = (total_intake / user.daily_goal) * 100 if user.daily_goal > 0 else 0
        achieved = total_intake >= user.daily_goal
        return {
            'total_intake': total_intake,
            'remaining': remaining,
            'percentage': round(percentage, 2),
            'goal': user.daily_goal,
            'achieved': achieved
        }

    @staticmethod
    def get_intake_by_date(water_intake: WaterIntake):
        date = water_intake.date or datetime.now(pytz.timezone('America/Sao_Paulo')).date()
        user_id = str(water_intake.user_id)
        intakes = WaterIntake.query.filter_by(user_id=user_id).filter(db.func.date(WaterIntake.date) == date).all()
        user = UserService.get_user(user_id)
        intake_summary = WaterIntakeService._calculate_intake_summary(user, intakes)
        intake_summary['date'] = date.strftime('%d-%m-%Y')
        return intake_summary
    
    @staticmethod
    def get_all_intake(user_id):
        intakes = WaterIntake.query.filter_by(user_id=user_id).all()
        daily_intakes = {}
        for intake in intakes:
            date_str = intake.date.date().strftime('%d-%m-%Y')
            if date_str not in daily_intakes:
                daily_intakes[date_str] = []
            daily_intakes[date_str].append(intake)

        user = UserService.get_user(user_id)
        consolidated_intakes = [
            {**WaterIntakeService._calculate_intake_summary(user, intake_on_date), 'date': date}
            for date, intake_on_date in daily_intakes.items()
        ]
        return consolidated_intakes
