# Many thanks to Jame's Briggs for his post on how to make an API in python
# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
#
# And also many thanks to https://pypi.org/project/RPi.bme280/ for example code for
# accessing the bme280
#
# Both projects are under the MIT license.

import smbus2
import bme280
from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


# TODO: See if it is possible to simplify this down to one class 
#       that presents the requested data based on the entrypoint name.

# provide the compensated temperature data rounded to 2 decimal places
class Temperature(Resource):
    def get(self):
        port = 1
        address = 0x77
        bus = smbus2.SMBus(port)

        calibration_params = bme280.load_calibration_params(bus, address)
        result = round(bme280.sample(bus, address, calibration_params).temperature, 2)
        return result

# provide the compensated pressure data (bme280 presents this in hPa)rounded to 2 decimal places
class Pressure(Resource):
    def get(self):
        port = 1
        address = 0x77
        bus = smbus2.SMBus(port)
        calibration_params = bme280.load_calibration_params(bus, address)
        result = round(bme280.sample(bus, address, calibration_params).pressure, 2)
        return result

# provide the compensated humidity data as a percentage rounded to 2 decimal places
class Humidity(Resource):
    def get(self):
        port = 1
        address = 0x77
        bus = smbus2.SMBus(port)

        calibration_params = bme280.load_calibration_params(bus, address)
        result = round(bme280.sample(bus, address, calibration_params).humidity, 2)
        return result

# Create API entry points
api.add_resource(Temperature, '/temperature')  # '/temperature' is our entry point
api.add_resource(Pressure, '/pressure')  # '/pressure' is our entry point
api.add_resource(Humidity, '/humidity')  # '/humidity' is our entry point

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # run our Flask app
