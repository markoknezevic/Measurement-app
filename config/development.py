import os
from config import Config


class Development(Config):
    ENV_TYPE = "Dev"

    DB_NAME = 'praksa_baza'
    DB_USER = "marko"
    DB_PASSWD = "123456"
    # DB_HOST = "127.0.0.1"
    # DB_PORT = 5432

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
