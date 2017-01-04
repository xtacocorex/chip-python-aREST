#!flask/bin/python

# aREST style API for controlling the CHIP via JSON and CHIP_IO
# Robert Wolterman, 2016
# Port from node.js to Python
# https://github.com/marcoschwartz/pi-aREST/blob/master/index.js
# Analog code adapted from:
# https://github.com/marcoschwartz/aREST-ESP8266/blob/master/aREST.lua

# Module Imports
from flask import Flask, jsonify, abort, request
import CHIP_IO.GPIO as GPIO
import CHIP_IO.PWM as PWM
import CHIP_IO.SOFTPWM as SPWM
import CHIP_IO.LRADC as LRADC
import CHIP_IO.OverlayManager as OM
import CHIP_IO.Utilities as UT
import random
import math
import copy
import sys
import paho.mqtt.client as mqtt

# Flask App
app = Flask(__name__)

# Global Variables
CHIP_INFO = {
        "id" : "001",
        "name" : "CHIPDEV",
        "hardware" : "chip",
        "connected" : False
        }
VARIABLES = {}
FUNCTIONS = {}
PINS_IN_USE = []

# Functions
def set_id(id):
    CHIP_INFO["id"] = id

def set_name(name):
    CHIP_INFO["name"] = name

def set_hardware(hw):
    CHIP_INFO["hardware"] = hw

def variable(name,value):
    VARIABLES[name] = value

def function(name,funct):
    FUNCTIONS[name] = funct

def make_id(mylen):
    text = ""
    possible = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in xrange(mylen):
        text += possible[int(math.floor(random.random() * len(possible)))]
    return text

# ==== API Basic Data ====
# Get the basic data
@app.route('/', methods=['GET'])
@app.route('/id', methods=['GET'])
def index():
    CHIP_INFO["connected"] = True
    return jsonify(CHIP_INFO)

# Get and Set Variables
# Execute functions
@app.route('/<string:variable>', methods=['GET','PUT','POST'])
def get_variables(variable=None):
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True

    if variable in VARIABLES:
        if request.method == 'GET':
            resp["connected"] = True
            resp[variable] = VARIABLES[variable]
        elif request.method in ['PUT','POST']:
            value = request.args.get('value')
            resp["connected"] = True
            VARIABLES[variable] = value
            resp[variable] = value

    if variable in FUNCTIONS:
        # Handle function arguments
        if request.args:
            ddict = request.args.to_dict()
            rtn = FUNCTIONS[variable](**ddict)
            resp["return_value"] = rtn
        else:
            rtn = FUNCTIONS[variable]()
            resp["return_value"] = rtn

    return jsonify(resp)

# ==== CHIP_IO Basics ====
# Get the CHIP_IO Version
@app.route('/version', methods=['GET'])
def get_chipio_version():
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True
    resp["message"] = GPIO.VERSION
    return jsonify(resp)

# ==== GPIO ====
# Digital Write
@app.route('/digital/<string:pin>/<int:value>', methods=['GET','PUT','POST'])
def digital_write_command(pin,value):
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True

    pin = pin.upper()

    # Setup pin if it isn't already and then add it
    if pin not in PINS_IN_USE:
        GPIO.setup(pin,GPIO.OUT)
        PINS_IN_USE.append(pin)

    # Write data to the pin
    if value == 0:
        resp["message"] = "Writing 0 to " + pin
        GPIO.output(pin,GPIO.LOW)
    elif value == 1:
        resp["message"] = "Writing 1 to " + pin
        GPIO.output(pin,GPIO.HIGH)
    else:
        resp["message"] = "Invalid value specified for " + pin

    return jsonify(resp)

# Digital Read
@app.route('/digital/<string:pin>/r', methods=['GET'])
@app.route('/digital/<string:pin>', methods=['GET'])
def digital_read_command(pin):
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True

    pin = pin.upper()

    # Setup pin if it isn't already and then add it
    if pin not in PINS_IN_USE:
        GPIO.setup(pin,GPIO.IN)
        PINS_IN_USE.append(pin)

    # Read the pin
    resp["message"] = GPIO.input(pin)

    return jsonify(resp)

# Digital Cleanup All
@app.route('/digital/cleanup', methods=['GET'])
def digital_pin_cleanup():
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True

    PINS_IN_USE = []
    GPIO.cleanup()

    resp["message"] = "All GPIO pins cleaned up"

    return jsonify(resp)

#TODO: Add Digital Cleanup for a Single Pin (dependent upon CHIP_IO feature #43)

# ==== PWM ====


# ==== SOFTPWM ====


# ==== LRADC ====
@app.route('/analog/<mode>', methods=['GET'])
@app.route('/analog/<string:mode>/<string:dat>', methods=['GET','PUT','POST'])
def get_lradc_data(mode,dat=None):
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True
    resp["mode"] = mode
    # Get Sample Rate
    if mode == "sample_rate" and dat == None and request.method == 'GET':
        resp["message"] = LRADC.get_sample_rate()
    # Set Sample Rate
    elif mode == "sample_rate" and dat != None and request.method in ['GET','PUT','POST']:
        dat = float(dat)
        if dat in [32.25,62.5,125,250]:
            resp["message"] = "Setting LRADC Sample Rate to " + str(dat)
            LRADC.set_sample_rate(dat)
    # Scale Factor
    elif mode == "scale_factor" and request.method == 'GET':
        resp["message"] = LRADC.get_scale_factor()
    # Get Data
    elif (mode == "full" or mode == "raw") and request.method == 'GET':
        dat = int(dat)
        if dat not in [0,1]:
            abort(404)
        elif dat == 0:
            if mode == "full":
                resp["message"] = LRADC.get_chan0()
            elif mode == "raw":
                resp["message"] = LRADC.get_chan0_raw()
        elif dat == 1:
            if mode == "full":
                resp["message"] = LRADC.get_chan1()
            elif mode == "raw":
                resp["message"] = LRADC.get_chan1_raw()
    else:
        resp["message"] = "invalid command"
    return jsonify(resp)

# ==== Utilities ====
@app.route('/unexport_all', methods=['GET'])
def unexport_all_pins():
    UT.unexport_all()
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True
    resp["message"] = "Unexporting all the Pins"
    return jsonify(resp)

@app.route('/1v8_pin/<string:command>', methods=['GET'])
@app.route('/1v8_pin/<string:command>/<float:voltage>', methods=['GET','PUT','POST'])
def handler_1v8pin(command,voltage=None):
    resp = copy.deepcopy(CHIP_INFO)
    resp["connected"] = True

    # If the command is "voltage" we are requesting the current voltage setting
    if command == "voltage":
        resp["message"] = "1.8V Pin Current Voltage: " + str(UT.get_1v8_pin_voltage())
    # Disable the 1v8 Pin
    elif command == "disable":
        resp["message"] = "Disabling the 1.8V Pin"
        UT.disable_1v8_pin()
    elif command == "enable":
        # Enable the 1v8 Pin
        voltage = float(voltage)
        if voltage not in [1.8, 2.0, 2.6, 3.3]:
            resp["message"] = "invalid voltage specified"
        else:
            resp["message"] = "Enabling the 1.8V Pin to " + str(voltage)
            UT.set_1v8_pin_voltage(voltage)
    else:
        resp["message"] = "invalid command"

    return jsonify(resp)

# ==== The REST App ====
# Actual Rest App
def RestApp(host="0.0.0.0",port=1883,debug=False):
    try:
        app.run(host=host,port=port,debug=debug)
    except KeyboardInterrupt:
        sys.exit(1)

# DEBUG Testing
if __name__ == '__main__':
    RestApp(debug=True)

