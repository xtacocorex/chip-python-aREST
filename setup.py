import distribute_setup
distribute_setup.use_setuptools()
from setuptools import setup, Extension, find_packages

classifiers = ['Development Status :: 3 - Alpha',
               'Operating System :: POSIX :: Linux',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: Home Automation',
               'Topic :: System :: Hardware']

setup(name             = 'CHIP_aREST',
      version          = '0.2.0',
      author           = 'Robert Wolterman',
      author_email     = 'robert.wolterman@gmail.com',
      description      = 'A module to control the CHIP IO channels via a REST API',
      long_description = open('README.rst').read() + open('CHANGELOG.rst').read(),
      license          = 'MIT',
      keywords         = 'CHIP NextThingCo IO GPIO PWM ADC REST',
      url              = 'https://github.com/xtacocorex/CHIP_aREST/',
      classifiers      = classifiers,
      install_requires = [ "flask", "CHIP_IO", "requests", "paho-mqtt" ],
      packages         = [ "CHIP_aREST" ],
      scripts          = [ "examples/chip-arest-basic.py" ])

