from flask_restplus import Resource
from flask_app.measurements import measurement_api
from flask import request
from flask_app import db
from flask_app.measurements.models import Measurement
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask_app.measurements.schemas import MeasurementGetSchema, MeasurementPostSchema
from marshmallow import ValidationError

measurement_get_schema = MeasurementGetSchema()
measurement_post_schema = MeasurementPostSchema()


@measurement_api.route("/")
@measurement_api.route("/<int:measurement_id>")
class MeasurementApi(Resource):

    def post(self):
        try:
            measurement_dict = measurement_post_schema.load(request.get_json(force=True))
            measurement = Measurement(**measurement_dict)
            db.session.add(measurement)
            db.session.commit()

        except SQLAlchemyError as e:
            print("SQLAlchemy error {}".format(e))
            return {'message': 'Database error'}, 500
        except ValidationError as e:
            print("Validation error:: {}".format(e))
            return {'message': f'Validation error {e}'}, 500
        except Exception as e:
            print("Unknown error:: {}".format(e))
            return {'message': 'Unknown error'}, 500

        return {'message': 'Success!'}, 200



    def get(self, measurement_id):
        try:
            measurement = db.session. \
                query(Measurement). \
                filter(Measurement.id == measurement_id). \
                one()

        except NoResultFound as error:
            print(f"No result found for id: {measurement_id}")
            print(f"Error: {error}")
            return {'message': 'No result found.'}, 404

        except MultipleResultsFound as error:
            print(f"Multiple results found for id: {measurement_id}")
            print(f"Error: {error}")
            return {'message': 'Database error.'}, 500

        except SQLAlchemyError as sqlalchemy_error:
            print(f"SqlAlchemy error:: {sqlalchemy_error}")
            return {'message': 'Database error.'}, 500

        except ValidationError as e:
            print("Validation error:: {}".format(e))
            return {'message': f'Validation error {e}'}, 500

        except Exception as server_error:
            print(f"Server error:: {server_error}")
            return {'message': 'Server error.'}, 500

        return measurement_get_schema.dump(measurement), 200

