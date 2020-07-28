"""
This module manages the configuration of the Flask app.
"""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('SECRET_KEY')
    DB_NAME = "production-db"

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASEDIR, 'data/yahtzee.db')
    SQLALCHEMY_ECHO = True

    SESSION_COOKIE_SECURE = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


class TestingConfig(Config):
    TESTING = True

    DB_NAME = "development-db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' \
        + os.path.join(BASEDIR, 'data/yahtzee.db')
    SQLALCHEMY_ECHO = True

    SESSION_COOKIE_SECURE = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
