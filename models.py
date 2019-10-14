from app import db
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Mesurment(db.Model):
    __tablename__ = 'measurements'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(Integer, nullable=False)
    air_quality = db.Column(Integer, nullable=False)
    humidity = db.Column(Integer, nullable=False)
    timestamp = db.Column(DateTime, nullable=False, default=datetime.utcnow())
