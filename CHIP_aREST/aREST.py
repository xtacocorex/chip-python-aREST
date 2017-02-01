#!flask/bin/python

# aREST style API for controlling the CHIP via JSON and CHIP_IO
# Robert Wolterman, 2016
#
# Port from node.js to Python
# https://github.com/marcoschwartz/pi-aREST/blob/master/index.js
#
# Analog code adapted from:
# https://github.com/marcoschwartz/aREST-ESP8266/blob/master/aREST.lua
#
# All other code I came up with to mimic the style

# Module Imports
from flask import Flask, jsonify, request
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
import signal
import paho.mqtt.client as mqtt

# Signal Handling
def sig_handler(signal, frame):
    OM.unload("PWM0")
    GPIO.cleanup()
    PWM.cleanup()
    SPWM.cleanup()
    UT.disable_1v8_pin()
    sys.exit(0)

signal.signal(signal.SIGTERM, sig_handler)

# Classes
class CHIP_RestAPI(Flask):
    def __init__(self, *args, **kwargs):
        super(CHIP_RestAPI, self).__init__(*args, **kwargs)
        self.CHIP_INFO = {
            "id" : "001",
            "name" : "CHIPDEV",
            "hardware" : "chip",
            "connected" : False
        }
        self.VARIABLES = {}
        self.FUNCTIONS = {}
        self.PINS_IN_USE = []

    def make_id(self,mylen):
        text = ""
        possible = "abcdefghijklmnopqrstuvwxyz0123456789"
        for i in xrange(mylen):
            text += possible[int(math.floor(random.random() * len(possible)))]
        return text

    def set_id(self,id):
        self.CHIP_INFO["id"] = id

    def get_id(self):
        return self.CHIP_INFO["id"]

    def set_name(self,name):
        self.CHIP_INFO["name"] = name

    def get_name(self):
        return self.CHIP_INFO["name"]

    def set_hardware(self,hw):
        self.CHIP_INFO["hardware"] = hw

    def get_hardware(self):
        return self.CHIP_INFO["hardware"]

    def set_variable(self,name,value):
        self.VARIABLES[name] = value

    def get_variable(self,name):
        if name in self.VARIABLES:
            return self.VARIABLES[name]
        else:
            return -1

    def set_function(self,name,funct):
        self.FUNCTIONS[name] = funct

    def api_debug(self):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True
        resp["message"] = "Debug Data"
        resp["variables"] = self.VARIABLES
        resp["functions"] = self.FUNCTIONS
        resp["pins in use"] = self.PINS_IN_USE
        return jsonify(resp)

    def api_chipio_version(self):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True
        resp["message"] = GPIO.VERSION
        return jsonify(resp)

    def api_get_variables(self,variable,req_method,req_args):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True

        if variable in self.VARIABLES:
            if req_method == 'GET':
                resp["connected"] = True
                resp[variable] = self.VARIABLES[variable]
            elif req_method in ['PUT','POST']:
                value = req_args.get('value')
                resp["connected"] = True
                self.VARIABLES[variable] = value
                resp[variable] = value
            elif req_method == 'DELETE':
                tmp = self.VARIABLES.pop(variable,None)
                resp["message"] = "Variable {0} deleted".format(variable)
                
        if variable in self.FUNCTIONS:
            #  Handle function arguments
            if req_args:
                ddict = req_args.to_dict()
                rtn = self.FUNCTIONS[variable](**ddict)
                resp["return_value"] = rtn
            else:
                rtn = self.FUNCTIONS[variable]()
                resp["return_value"] = rtn

        return jsonify(resp)

    def api_digital_cleanup(self):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True
        resp["message"] = "All GPIO pins cleaned up"

        self.PINS_IN_USE = []
        GPIO.cleanup()

        return jsonify(resp)

    def api_digital_pin_cleanup(self,pin):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True

        if not self.PINS_IN_USE:
            resp["message"] = "No pins currently setup"
        else:
            pin = pin.upper()

            if pin not in self.PINS_IN_USE:
                resp["message"] = "Pin not previously in use"
            else:
                resp["message"] = "Cleaning up %s" % pin
                GPIO.cleanup(pin)
                self.PINS_IN_USE.remove(pin)

        return jsonify(resp)

    def api_digital_write(self,pin,value):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True

        pin = pin.upper()

        # Setup pin if it isn't already and then add it
        if pin not in self.PINS_IN_USE:
            GPIO.setup(pin,GPIO.OUT)
            self.PINS_IN_USE.append(pin)

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

    def api_digital_read(self,pin):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True

        pin = pin.upper()

        # Setup pin if it isn't already and then add it
        if pin not in self.PINS_IN_USE:
            GPIO.setup(pin,GPIO.IN)
            self.PINS_IN_USE.append(pin)

        # Read the pin
        resp["message"] = GPIO.input(pin)

        return jsonify(resp)

    def api_lradc_data(self,mode,dat,req_method,req_args):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True
        resp["mode"] = mode
        # Get Sample Rate
        if mode == "sample_rate" and dat == None and req_method == 'GET':
            resp["message"] = LRADC.get_sample_rate()
        # Set Sample Rate
        elif mode == "sample_rate" and dat != None and req_method in ['GET','PUT','POST']:
            dat = float(dat)
            if dat in [32.25,62.5,125,250]:
                resp["message"] = "Setting LRADC Sample Rate to " + str(dat)
                LRADC.set_sample_rate(dat)
        # Scale Factor
        elif mode == "scale_factor" and req_method == 'GET':
            resp["message"] = LRADC.get_scale_factor()
        # Get Data
        elif (mode == "full" or mode == "raw") and req_method == 'GET':
            dat = int(dat)
            if dat not in [0,1]:
                resp["message"] = "Invalid ADC Channel Specified"
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

    def api_unexport_all_pins():
        UT.unexport_all()
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True
        resp["message"] = "Unexporting all the Pins"
        return jsonify(resp)

    def api_handle_1v8pin(command,voltage=None):
        resp = copy.deepcopy(self.CHIP_INFO)
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

    def api_pwm(self,chan,command,option,req_method,req_args):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True

        # Default the channel to PWM0
        # CHIP Pro will support PWM1
        cname = "PWM0"

        chan = int(chan)
        if chan not in [0]: #,1]:
            resp["message"] = "Invalid PWM Channel Specified"
            return jsonify(resp)
        else:
            if chan == 0:
                cname = "PWM0"
            elif chan == 1:
                cname = "PWM1"

        # Figure out our command
        if command == "start" and req_method == 'GET':
            # Load the overlay
            OM.load(cname)
            # Get the arguments
            duty_cycle = req_args.get('duty_cycle', 25.0)
            frequency = req_args.get('frequency', 200.0)
            polarity = req_args.get('polarity', 0)
            # Start the PWM
            PWM.start(cname,duty_cycle,frequency,polarity)
            resp["message"] = "Setting {0} to duty cycle: {1}, frequency: {2}, and polarity {3}".format(cname,duty_cycle,frequency,polarity)
        elif command == "stop" and req_method == 'GET':
            PWM.stop(chame)
            resp["message"] = "Stopping {0}".format(cname)
        elif command == "cleanup" and req_method == 'GET':
            # TODO: Handle per channel cleanup
            PWM.cleanup()
            OM.unload(cname)
            resp["message"] = "Cleaning up and unloading {0}".format(cname)
        elif command == "duty_cycle" and req_method in ['GET','PUT','POST']:
            PWM.set_duty_cycle(cname, float(option))
            resp["message"] = "Changing duty cycle on {0} to {1}".format(cname,option)
        elif command == "frequency" and req_method in ['GET','PUT','POST']:
            PWM.set_frequency(cname, float(option))
            resp["message"] = "Changing duty cycle on {0} to {1}".format(cname,option)
        return jsonify(resp)
        
    def api_softpwm(self,pin,command,option,req_method,req_args):
        resp = copy.deepcopy(self.CHIP_INFO)
        resp["connected"] = True

        # Figure out our command
        if command == "start" and req_method == 'GET':
            # Get the arguments
            duty_cycle = req_args.get('duty_cycle', 25.0)
            frequency = req_args.get('frequency', 35.0)
            polarity = req_args.get('polarity', 0)
            # Start the SoftPWM
            SPWM.start(pin,duty_cycle,frequency,polarity)
            resp["message"] = "Setting {0} to duty cycle: {1}, frequency: {2}, and polarity {3}".format(pin,duty_cycle,frequency,polarity)
        elif command == "stop" and req_method == 'GET':
            SPWM.stop(pin)
            resp["message"] = "Stopping {0}".format(pin)
        elif command == "cleanup" and req_method == 'GET':
            SPWM.cleanup(pin)
            resp["message"] = "Cleaning up {0}".format(pin)
        elif command == "duty_cycle" and req_method in ['GET','PUT','POST']:
            SPWM.set_duty_cycle(pin, float(option))
            resp["message"] = "Changing duty cycle on {0} to {1}".format(pin,option)
        elif command == "frequency" and req_method in ['GET','PUT','POST']:
            SPWM.set_frequency(pin, float(option))
            resp["message"] = "Changing duty cycle on {0} to {1}".format(pin,option)
        return jsonify(resp)

# Flask App
app = CHIP_RestAPI(__name__)

# User Functions
def set_id(id):
    app.set_id(id)

def set_name(name):
    app.set_name(name)

def set_hardware(hw):
    app.set_hardware(hw)

def variable(name,value):
    app.set_variable(name, value)

def function(name,funct):
    app.set_function(name,funct)

# ==== The REST App ====
# Actual Rest App
def RestApp(host="0.0.0.0",port=1883,debug=False):
    try:
        app.run(host=host,port=port,debug=debug)
    except KeyboardInterrupt:
        GPIO.cleanup()
        PWM.cleanup()
        SPWM.cleanup()
        UT.disable_1v8_pin()
        sys.exit(0)

# ==== API Basic Data ====
# Get the basic data
# GET: /
# GET: /id
@app.route('/', methods=['GET'])
@app.route('/id', methods=['GET'])
def index():
    app.CHIP_INFO["connected"] = True
    return jsonify(app.CHIP_INFO)

# Get and Set Variables
# Execute functions
# GET: /<variablename>
# PUT,POST: /<variablename>?value=<value>
# GET: /<functionname>
# GET: /<functionname>?value=<value>
@app.route('/<string:variable>', methods=['GET','PUT','POST','DELETE'])
def get_variables(variable=None):
    return app.api_get_variables(variable,request.method,request.args)

# ==== API DEBUG ====
# GET: /debug
@app.route('/debug', methods=['GET'])
def get_api_debug():
    return app.api_debug()

# ==== CHIP_IO Basics ====
# Get the CHIP_IO Version
# GET: /version
@app.route('/version', methods=['GET'])
def get_chipio_version():
    return app.api_chipio_version()

# ==== GPIO ====
# Digital Read and Cleanup
# GET: /digital/cleanup
# GET: /digital/cleanup/<pinname>
# GET: /digital/<pinname>/r
# GET: /digital/<pinname>
@app.route('/digital/<string:command>', defaults={'pin' : None}, methods=['GET'])
@app.route('/digital/<string:command>/<string:pin>', methods=['GET'])
def digital_read_cleanup(command,pin=None):
    # We want to cleanup
    if command == "cleanup":
        # If we have no mode specified (mode == pin)
        if pin == None:
            return app.api_digital_cleanup()
        # Do the pin cleanup, if the pin value isn't "r" for a read
        elif pin != "r":
            return app.api_digital_pin_cleanup(pin)
    else:
        # For the read, the pin name is the command
        return app.api_digital_read(command)

# Digital Write
# GET,PUT,POST: /digital/<pinname>/[0,1]
@app.route('/digital/<string:pin>/<int:value>', methods=['GET','PUT','POST'])
def digital_write_command(pin,value):
    return app.api_digital_write(pin,value)

# ==== PWM ====
# GET: /pwm/[0,1]/start?duty_cycle=<dutycycle>&frequency=<frequency>&polarity=[0,1]
# GET: /pwm/[0,1]/stop
# GET: /pwm/[0,1]/cleanup
# GET, PUT, POST: /pwm/[0,1]/duty_cycle/<dutycycle>
# GET, PUT, POST: /pwm/[0,1]/frequency/<frequency>
@app.route('/pwm/<int:chan>/<string:command>', methods=['GET','PUT','POST'])
@app.route('/pwm/<int:chan>/<string:command>/<string:option>', methods=['GET','PUT','POST'])
def pwm_all_commands(chan,command,option=None):
    return app.api_pwm(chan,command,option,request.method,request.args)

# ==== SOFTPWM ====
# GET: /softpwm/<pinname>/start?duty_cycle=<dutycycle>&frequency=<frequency>&polarity=[0,1]
# GET: /softpwm/<pinname>/stop
# GET: /softpwm/<pinname>/cleanup
# GET, PUT, POST: /softpwm/<pinname>/duty_cycle/<dutycycle>
# GET, PUT, POST: /softpwm/<pinname>/frequency/<frequency>
@app.route('/softpwm/<string:pin>/<string:command>', methods=['GET','PUT','POST'])
@app.route('/softpwm/<string:pin>/<string:command>/<string:option>', methods=['GET','PUT','POST'])
def softpwm_all_commands(pin,command,option=None):
    return app.api_softpwm(pin,command,option,request.method,request.args)

# ==== LRADC ====
# Methods
# GET: /analog/sample_rate
# GET: /analog/scale_factor
# GET: /analog/full/[0,1]
# GET: /analog/raw[0,1]
# GET,PUT,POST: /analog/sample_rate/[32.25,62.5,125,250]
@app.route('/analog/<mode>', methods=['GET'])
@app.route('/analog/<string:mode>/<string:dat>', methods=['GET','PUT','POST'])
def get_lradc_data(mode,dat=None):
    return app.api_lradc_data(mode,dat,request.method,request.args)

# ==== Utilities ====
# Methods
# GET: /unexport_all
@app.route('/unexport_all', methods=['GET'])
def unexport_all_pins():
    return app.api_unexport_all_pins()

# GET: /1v8_pin/voltage
# GET: /1v8_pin/disable
# GET,PUT,POST: 1v8_pin/enable/[1.8,2.0,2.6,3.3]
@app.route('/1v8_pin/<string:command>', methods=['GET'])
@app.route('/1v8_pin/<string:command>/<float:voltage>', methods=['GET','PUT','POST'])
def handler_1v8pin(command,voltage=None):
    return app.api_handle_1v8_pin()

# DEBUG Testing
if __name__ == '__main__':
    RestApp(debug=True)

