from flask_app import db
from sqlalchemy import Integer, DateTime
from datetime import datetime

class Measurement(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(Integer, primary_key=True)
    temperature = db.Column(Integer, nullable=False)
    air_quality = db.Column(Integer, nullable=False)
    humidity = db.Column(Integer, nullable=False)
    timestamp = db.Column(DateTime, nullable=False, default=datetime.utcnow())
