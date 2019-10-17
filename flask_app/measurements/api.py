from flask_restplus import Resource
from flask_app.measurements import measurement_api
from flask import request
from flask_app import db
from flask_app.measurements.models import Measurement
from sqlalchemy.exc import SQLAlchemyError


@measurement_api.route("/")
class MeasurementApi(Resource):

    def post(self):
        try:
            data = request.get_json(force=True)

            measurement = Measurement(
                temperature=data["temperature"],
                air_quality=data["air_quality"],
                humidity=data["humidity"])

            # mesaurement = Measurement(**data)

            db.session.add(measurement)
            db.session.commit()

        except SQLAlchemyError as e:
            print("SQLAlchemy error {}".format(e))
            return {'message': 'Database error'}, 500
        except Exception as e:
            print("Unknown error:: {}".format(e))
            return {'message': ''}, 500

        return {'message': 'Success!'}, 200



    def get(self):
        return {'message': "message"}, 200



# @measurement_api.route('/pera')
# @measurement_api.route('/pera/<int:id>')
# @measurement_api.route('/nije_pera')
# class MeasurementApi2(Resource):
#     pass
#
# @measurement_api.route('/treca')
# class MeasurementApi3(Resource):
#     pass
