from marshmallow import Schema, fields, validates_schema, ValidationError, validates


class MeasurementGetSchema(Schema):
    id = fields.Int(required=True)
    temperature = fields.Int(required=True)
    air_quality = fields.Int(required=True, allow_none=False)
    humidity = fields.Int(required=True, allow_none=False)
    timestamp = fields.DateTime(required=True, allow_none=False)


class MeasurementPostSchema(Schema):
    id = fields.Int(required=False)
    temperature = fields.Int(required=True)
    air_quality = fields.Int(required=True, allow_none=False)
    humidity = fields.Int(required=True, allow_none=False)
    timestamp = fields.DateTime(required=False, allow_none=False)

    @validates_schema
    def data_validation(self, data, **kwargs):
        if data["temperature"] < 0:
            raise ValidationError("Wrong temperature")

        if data["air_quality"] < 0 or data["air_quality"] > 100:
            raise ValidationError("Wrong air quality")

        if data["humidity"] < 0 or data["humidity"] > 100:
            raise ValidationError("Wrong humidity")
