import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '123456')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///water_tracker.db')
    TESTING = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    pass
