from flask import Flask, jsonify, make_response
from flask_cors import CORS
import board
import adafruit_tsl2591
from adafruit_bme280 import basic as adafruit_bme280

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Initialize I2C and sensors
try:
    i2c = board.I2C()
    tsl2591 = adafruit_tsl2591.TSL2591(i2c)
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
except Exception as e:
    # Log error if I2C or sensors initialization fails
    print(f"Error initializing sensors: {e}")

@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    try:
        # Fetch data from sensors
        lux = tsl2591.lux
        visible_light = tsl2591.visible
        infrared_light = tsl2591.infrared
        full_spectrum = tsl2591.full_spectrum
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure
        

        # Create a data dictionary
        data = {
            "lux": f"{lux:.2f}",
            "visible": visible_light,
            "infrared": infrared_light,
            "full_spectrum": full_spectrum,
            "temperature": f"{temperature:.2f}",
            "humidity": f"{humidity:.2f}",
            "pressure": f"{pressure:.2f}"
        }
        return jsonify(data), 200  # Return data with a 200 OK status
    except Exception as e:
        # If any error occurs, return a 500 Internal Server Error with an error message
        error_message = f"Failed to retrieve sensor data: {e}"
        print(error_message)
        return make_response(jsonify({"error": error_message}), 500)

@app.route('/is_sensor_on', methods=['GET'])
def check_sensor_status():
    try:
        bme280_status = get_bme280_data is not None
        tsl2591_status = get_tsl2591_data is not None
    except Exception:
        return jsonify({"status": "degraded", "bme280": bme280_status, "tsl2591": tsl2591_status})
    return jsonify({"status": "healthy", "bme280": bme280_status, "tsl2591": tsl2591_status})


@app.route('/bme280', methods=['GET'])
def get_bme280_data():
    data = {"temperature": f"{bme280.temperature:.2f}",
            "humidity": f"{bme280.humidity:.2f}",
            "pressure":f"{bme280.pressure:.2f}"
            }
    return jsonify(data)

@app.route('/tsl2591', methods=['GET'])
def get_tsl2591_data():
    data = {"lux": f"{tsl2591.lux:.2f}",
            "visible": tsl2591.visible,
            "infrared": tsl2591.infrared,
            "full_spectrum": tsl2591.full_spectrum
            }
    return jsonify(data)

@app.errorhandler(404)
def not_found(error):
    # Custom 404 error handler
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    # Custom 500 error handler
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
