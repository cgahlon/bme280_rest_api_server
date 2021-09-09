# Many thanks to Jame's Briggs for his post on how to make an API in python
# https://towardsdatascience.com/the-right-way-to-build-an-api-with-python-cd08ab285f8f
#
# And also many thanks to https://pypi.org/project/RPi.bme280/ for example code for
# accessing the bme280
#
# Both of the above projects are under the MIT license, as is this one.

import smbus2
import bme280
from flask import Flask, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# TODO: See if it is possible to simplify this down to one class 
#       that presents the requested data based on the entrypoint name.

# Provide open metrics formatted data (i.e. prometheus)
class PrometheusMetrics(Resource):
    def get(self):
        port = 1
        address = 0x77
        bus = smbus2.SMBus(port)
        calibration_params = bme280.load_calibration_params(bus, address)
        data = bme280.sample(bus, address, calibration_params)

        def create_formatted():
            def print_metrics(name, value, text):
                a = str(f'# HELP {name} {text}\n')
                b = str(f'# TYPE {name} gauge\n')
                c = str(f'{name} {value}\n')
                d = '%s%s%s' % (a,b,c)
                return d
            temperature = str(print_metrics("temperature", str(round(data.temperature, 2)), "Temperature in celsius"))
            pressure = str(print_metrics("pressure", str(round(data.temperature, 2)), "Pressure in Pascal(Pa)"))
            humidity = str(print_metrics("humidity", str(round(data.temperature, 2)), "Humidity percentage"))
            result = '''%s%s%s''' % (temperature,pressure,humidity)
            return result
        response = make_response(create_formatted(), 200)
        response.mimetype = "text/plain"
        return response

# Create API entry points
api.add_resource(PrometheusMetrics, '/metrics')  # '/prometheus_metrics' is our entry point

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9100)  # run our Flask app
