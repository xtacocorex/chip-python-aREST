chip_python_aREST
============================
A REST API for controlling CHIP GPIO

Manual::

For Python2.7::

    sudo apt-get update
    sudo apt-get install git build-essential python-dev python-pip flex bison python-flask -y
    git clone git://github.com/xtacocorex/chip_python_aREST.git
    cd chip_python_aREST
    sudo python setup.py install

For Python3 (**UNTESTED**)::

    sudo apt-get update
    sudo apt-get install git build-essential python3-dev python3-pip flex bison python-flask -y
    git clone git://github.com/xtacocorex/chip_python_aREST.git
    cd chip_python_aREST
    sudo python3 setup.py install

CHIP_IO is required to use this library, code and instructions are here: https://github.com/xtacocorex/CHIP_IO
Scripts using this library will need to be run with root permissions (sudo or started at boot by init script).


Usage
--------

**Example Script**

The following is an example script that details a basic way to instantiate the REST API on your CHIP::

    import CHIP_aREST.aREST as aREST

    # Setup the id
    # The id is a special identifier for your CHIP
    aREST.set_id('5gad42')

    # Setup the name
    # The name can be anything you want
    aREST.set_name("My Local CHIP")

    # Setup the hardware type
    # Not really needed until CHIP_IO get CHIP Pro support
    aREST.set_hardware("chip")

    # This is where any variables and functions would be setup

    # Start the API
    # Debug can be turned on/off
    # Keep the host 0.0.0.0 to allow for local network access
    # Port can be whatever you want it to be
    aREST.RestApp(host="0.0.0.0"<Plug>PeepOpenort=3000,debug=True)

The API also supports user specified variables and functions::

    # First create the variable
    temperature = 25.2
    # Then add it to the API
    aREST.variable("temperature",temperature)

    # For funtions, we need to define it first
    # Functions can have arguments and they can be fed in with url parameters
    def myfunction():
        # you can do whatever you want here
        # CHIP_IO Specific calls
        # crazy math
        # or in this case
        return "myfunction was called, howdy!"

    # Now we add it to the API
    # Make sure you don't add the () to the function
    aREST.function("functiontest",myfunction)

Cloud features TBD.

Example scripts are found in the examples folder.  They are also installed into /usr/local/bin/.

REST API
---------

For local instances of the API, you can access the CHIP via:

    http://192.168.0.5:3000/

Replace the IP address with the one for your CHIP.  If you have avahi installed on your CHIP, you can replace the IP address with <hostname>.local.

All of the REST API are detailed in the tables below.  Note the HTTP Method used for the call.  Not everything uses a normal HTTP GET method.

If you use a web browser to send the URL to the CHIP, you are limited to the GET method.

The curl program installed in Linux or MacOS/OS X can be used to test the API::

    curl -X  GET http://chipdev.local:3000/digital/csid0/1
    curl -X  GET http://chipdev.local:3000/temperature
    curl -X  PUT http://chipdev.local:3000/temperature?value=-24.2

**Basics**

  +------------------+-------------------------------+------------------------------------------------------+
  | **Method**       | **Command**                   | **Description**                                      |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /                             | Basic Info                                           |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /id                           | Basic Info                                           |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /debug                        | Dump all data                                        |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /<variablename>               | Get value of <variablename>                          |
  +------------------+-------------------------------+------------------------------------------------------+
  | DELETE           | /<variablename>               | Delete <variablename>                                |
  +------------------+-------------------------------+------------------------------------------------------+
  | PUT, POST        | /<variablename>?value=<value> | Set <variablename> to <value>                        |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /<functionname>               | Get value of <functionname>                          |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /<functionname>?value=<value> | Get value of <functionname> with <value> as input    |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /version                      | Get current CHIP_IO version                          |
  +------------------+-------------------------------+------------------------------------------------------+

**GPIO**

  +------------------+-------------------------------+------------------------------------------------------+
  | **Method**       | **Command**                   | **Description**                                      |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET, PUT, POST   | /digital/<pinname>/[0,1]      | Digital Write 0 or 1 to <pinname>                    |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /digital/<pinname>            | Digital Read <pinname>                               |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /digital/<pinname>/r          | Digital Read <pinname>                               |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /digital/cleanup              | Cleanup all GPIO Pins                                |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /digital/cleanup/<pinname>    | Cleanup only GPIO Pin: <pinname>                     |
  +------------------+-------------------------------+------------------------------------------------------+

**PWM**

  +------------------+-----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
  | **Method**       | **Command**                                               | **Description**                                                                                                   |
  +------------------+-----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
  | GET              | /pwm/0/start?duty_cycle=[0.0-100.0]&frequency=<frequency> | Start PWM0 with duty cycle and frequency.  duty_cycle and frequency are optional, they default to 25.0% and 200.0 |
  +------------------+-----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
  | GET              | /pwm/0/stop                                               | Stop PWM0                                                                                                         |
  +------------------+-----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
  | GET              | /pwm/0/cleanup                                            | Cleanup PWM0                                                                                                      |
  +------------------+-----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
  | GET, PUT, POST   | /pwm/0/duty_cycle/[0.0-100.0]                             | Change PWM0 Duty Cycle                                                                                            |
  +------------------+-----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+
  | GET, PUT, POST   | /pwm/0/frequency/<frequency>                              | Change PWM0 Frequency                                                                                             |
  +------------------+-----------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------+

**Software PWM**

  +------------------+-----------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
  | **Method**       | **Command**                                                           | **Description**                                                                                                                   |
  +------------------+-----------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
  | GET              | /softpwm/<pinname>/start?duty_cycle=[0.0-100.0]&frequency=<frequency> | Start SoftPWM on <pinname> with duty cycle and frequency.  duty_cycle and frequency are optional, they default to 25.0% and 35.0  |
  +------------------+-----------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
  | GET              | /softpwm/<pinname>/stop                                               | Stop SoftPWM on <pinname>                                                                                                         |
  +------------------+-----------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
  | GET              | /softpwm/<pinname>/cleanup                                            | Cleanup SoftPWM on <pinname>                                                                                                      |
  +------------------+-----------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
  | GET, PUT, POST   | /softpwm/<pinname>/duty_cycle/[0.0-100.0]                             | Change SoftPWM Duty Cycle on <pinname>                                                                                            |
  +------------------+-----------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+
  | GET, PUT, POST   | /softpwm/<pinname>/frequency/<frequency>                              | Change SoftPWM Frequency on <pinname>                                                                                             |
  +------------------+-----------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------+

**LRADC**

  +------------------+-------------------------------------------+------------------------------------------------------+
  | **Method**       | **Command**                               | **Description**                                      |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET, PUT, POST   | /analog/sample_rate/[32.25,62.5,125,250]  | Set LRADC Sample Rate to 32.25, 62.5, 125, or 250    |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET              | /analog/sample_rate                       | Get currrent LRADC Sample Rate                       |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET              | /analog/scale_factor                      | Get LRADC Scale Factor                               |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET              | /analog/raw/[0,1]                         | Get raw LRADC output for channel 0 or 1              |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET              | /analog/full/[0,1]                        | Get full LRADC output for channel 0 or 1             |
  +------------------+-------------------------------------------+------------------------------------------------------+

  **Utilities**

  +------------------+-------------------------------------------+------------------------------------------------------+
  | **Method**       | **Command**                               | **Description**                                      |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET, PUT, POST   | /1v8_pin/enable/[1.8,2.0,2.6,3.3]         | Enable 1.8V Pin to output 1.8, 2.0, 2.6, or 3.3V     |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET              | /1v8_pin/voltage                          | Get currrent 1.8V Pin voltage setting                |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET              | /1v8_pin/disable                          | Disable 1.8V Pin                                     |
  +------------------+-------------------------------------------+------------------------------------------------------+
  | GET              | /unexport_all                             | Backup function to unexport all GPIO                 |
  +------------------+-------------------------------------------+------------------------------------------------------+

Credits
--------

Marco Schwartz for the original pi-aREST node.js code that was used as a basis for this code.
(https://github.com/marcoschwartz/pi-aREST)

License
-------

CHIP Python aREST by Robert Wolterman, released under the MIT License.
