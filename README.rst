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
  | GET              | /debug                        |  Dump all data                                       |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /<variablename>               | Get value of <variablename>                          |
  +------------------+-------------------------------+------------------------------------------------------+
  | PUT, POST        | /<variablename>?value=<value> | Set <variablename> to <value>                        |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /<functionname>               | Get value of <functionname>                          |
  +------------------+-------------------------------+------------------------------------------------------+
  | GET              | /<functionname>?value=<value> | Get value of <functionname> with <value> as input    |
  +------------------+-------------------------------+------------------------------------------------------+

**GPIO**

**PWM**

TBD

**Software PWM**

TBD

**LRADC**

**Utilities**


Credits
--------

Marco Schwartz for the original pi-aREST node.js code that was used as a basis for this code.
(https://github.com/marcoschwartz/pi-aREST)

License
-------

CHIP Python aREST by Robert Wolterman, released under the MIT License.
