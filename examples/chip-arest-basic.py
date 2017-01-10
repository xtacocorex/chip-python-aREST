#!/usr/bin/env python
# Copyright (c) 2017 Robert Wolterman

# Basic example using the CHIP aREST API

# Module Imports
import CHIP_aREST.aREST as aREST

# Setup the Device Info
aREST.set_id('id4311')
# or
#aREST.set_id("Xy56E1")
aREST.set_name("MY_CHIP")
# In the future, this would be used to differentiate a CHIP and CHIP Pro
aREST.set_hardware("chip")

# Variable Examples
temperature = 21.2
humidity = 95.2
aREST.variable("temperature",temperature)
aREST.variable("humidity",humidity)

# Function Example
def myfunction():
    return "hello from myfunction!"

aREST.function("functiontest",myfunction)

# Start
aREST.RestApp(host="0.0.0.0",port=3000,debug=True)

