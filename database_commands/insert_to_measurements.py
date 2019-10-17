import random
from flask_app import db
from server import app
from flask_app.measurements.models import Measurement
from datetime import datetime, timedelta


def insert_random_measurement_data():
    for i in range(1000):
        random_temperature = random.randint(-30, 40)
        random_air_quality = random.randint(0, 100)
        random_humidity = random.randint(0, 100)
        random_date = datetime.utcnow() - timedelta(days=i)

        measurement = Measurement(temperature=random_temperature,
                                air_quality=random_air_quality,
                                humidity=random_humidity,
                                timestamp=random_date)

        db.session.add(measurement)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        try:
            insert_random_measurement_data()
        except Exception as e:
            print(e)
