import os
from config import Config


class Development(Config):
    ENV_TYPE = "Dev"

    DB_NAME = 'praksa_baza'
    DB_USER = "marko"
    DB_PASSWD = "123456"
    DB_HOST = "127.0.0.1"
    DB_PORT = 5432

    SQLALCHEMY_DATABASE_URI = "postgres://qfzpkprtsifydm" \
                              ":a206e17b674364a11d405801a1c00e237f869c5816d8658168d3b19858cf724f@ec2-54-228-252-67.eu" \
                              "-west-1.compute.amazonaws.com:5432/dcopatjjik6tdb "
