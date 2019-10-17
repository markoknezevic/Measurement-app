from flask import Blueprint
from flask_restplus import Api

APP_NAME = "measurements"

measurement_blueprint = Blueprint(APP_NAME,
                                  __name__,
                                  url_prefix="/{}".format(APP_NAME))

measurement_api = Api(measurement_blueprint)

from flask_app.measurements.api import *
