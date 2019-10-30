from flask_restplus import Resource
from flask_app.measurements import measurement_api
from flask import request
from flask_app import db
from flask_app.measurements.models import Measurement
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from flask_app.measurements.schemas import MeasurementGetSchema, MeasurementPostSchema
from marshmallow import ValidationError
from datetime import datetime
import math

measurement_get_schema = MeasurementGetSchema()
measurement_post_schema = MeasurementPostSchema()


@measurement_api.route("/latest")
class MeasurementsApiLast(Resource):
    def get(self):
        last_record = db.session.query(Measurement).order_by(Measurement.id.desc()).first()
        return measurement_get_schema.dump(last_record)


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


@measurement_api.route("/history")
class MeasurementsApi2(Resource):
    def get(self):

        try:
            # proveravamo da li je "start" argumenat prosledjen
            if "start" in request.args:
                start = int(request.args["start"])
            else:
                start = 0

            # proveravamo da li je "end" argumenat prosledjen ako nije uzimamo danasnji datum
            if "end" in request.args:
                end = int(request.args["end"])
            else:
                end = datetime.utcnow().timestamp() * 1000

            # Konvertujemo datum iz milisekundi u datum
            start_date = datetime.fromtimestamp(start / 1000.0)
            end_date = datetime.fromtimestamp(end / 1000.0)

            # izvlacimo iz tabele measurements sve redove izmedju trazenih datuma
            list_of_measurements = db.session.query(Measurement).filter(Measurement.timestamp >= start_date,
                                                                        Measurement.timestamp <= end_date)
            # broj preuzetih redova iz tabele measurements
            number_of_elements = list_of_measurements.count()

            # proveravamo da li je prosledjen argumenat "limit" i da li je 0
            if "limit" in request.args and int(request.args["limit"]) != 0:
                limit = int(request.args["limit"])
                step = math.ceil(number_of_elements / limit)
            else:
                step = 1

        except ValueError as error:
            print(error)
            return {'Message': 'Wrong type of arguments'}

        except Exception as error:
            print(error)
            return {'Message': "Internal error :)"},

        return {"Measurements": [measurement_get_schema.dump(list_of_measurements[i]) for i in
                                 range(0, number_of_elements, step)]}, 200



