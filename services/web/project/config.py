import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") + os.getenv("DB_NAME")
    DB_NAME = os.getenv("DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENV = "development"
