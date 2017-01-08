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

For Python3::

    sudo apt-get update
    sudo apt-get install git build-essential python3-dev python3-pip flex bison python-flask -y
    git clone git://github.com/xtacocorex/chip_python_aREST.git
    cd chip_python_aREST
    sudo python3 setup.py install

CHIP_IO is required to use this library, code and instructions are here: https://github.com/xtacocorex/CHIP_IO

Usage
--------

TBD

REST API
---------

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

TBD

**Software PWM**

TBD

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
