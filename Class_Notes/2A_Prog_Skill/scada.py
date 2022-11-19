import random
import math
import datetime
import time
import numpy as np
from scipy.interpolate import interp1d
from blinkstick import blinkstick  # pylint: disable=import-error

"""scada.py provides a simple interface to the data aquaisition system (DAQ) needed for
the 2nd piece of coursework.  It provides a class called DAQ which contains the following methods

__init__() - initialise the DAQ using a student matriculation number. 
This is read from the blinkstick

connect_instrument(instrument) - select the instrument to be aquired

next_reading() - returns the next reading from the slected instrument when it is available.

trigger() - record the current time and send a reset signal to all instruments, starting the experiment. 

Four instruments are available:

* constant(level) - output a constant signal at the specified voltage.
* increasing - a signal which varies linearly in time, starting at the low voltage and rising to the high voltage over 
    a period of 60 seconds.
* decreasing - a signal which varies linearly in time, starting at the high voltage and falling to the low voltage over
    a period of 60 seconds. 
* coursework - signal used for the coursework, this varies over a period of 60 seconds and will include both low and 
    high values.
    
Written by David Ingram
School of Engineering
(c) The University of Edinburgh 2020, 2021
Licensed: CC-BY
"""


class Error(Exception):
    """ Class used to create errors """
    pass


class BlinkStickNotFound(Error):
    """Raised when no blinkstick is connected"""
    pass


class InvalidMatricNumber(Error):
    """Raised when no blinkstick is connected"""
    pass


class DAQ:
    REF_HIGH = +5.0  # high voltage limit on sensor
    REF_LOW = -5.0  # low voltage limit on sensor
    BITS = 10  # number of bits used to encode the signal
    DELTA_T = 0.5  # sample period (s)

    INSTRUMENTS = ["constant", "ramp up", "ramp down", "coursework"]

    def __init__(self, matric='s1234567', user='Manually specified', wait=True):
        """ create a new DAQ, with the specified id,
        this should be your matriculation number.
        """
        import re

        # find the ID from the blinkstick
        bstick = blinkstick.find_first()

        if bstick is None:
            student_id = matric
            owner = user
        else:
            student_id = bstick.get_info_block2()
            owner = bstick.get_info_block1()

        # check if this is a matric number
        if re.match('s\d{7}', student_id) is None:
            print(student_id, ' is not a valid matriculation number.')
            print('*** You must have configured your blinkstick with your name and matriculation number ***')
            raise InvalidMatricNumber

        self.instrument = 'None'
        self.Q = (self.REF_HIGH - self.REF_LOW) / 2 ** self.BITS
        self.identity = student_id
        random.seed(student_id)
        self.initialised = datetime.datetime.now()
        self.time = 0.0
        self.last_reading = time.time()
        print("DAQ {} Initialised {} Q={}".format(
            self.identity, self.initialised, self.Q))
        print("licensed to {}.".format(owner))

        self.wait = wait

    def connect(self, instrument, level=0):
        inst_type = self.INSTRUMENTS.index(instrument)

        if inst_type == 0:
            self.parameter = [level, 0.]
        elif inst_type == 1:
            self.parameter = [-4.5, 9 / 60]
        elif inst_type == 2:
            self.parameter = [+4.5, -9 / 60]
        elif inst_type == 3:
            x = [0, 5, random.uniform(8, 12),
                 random.uniform(15, 22), 30, random.uniform(38, 45),
                 random.uniform(47, 55), 57, 60]
            v = [-2.6, -2.55, -2.45,
                 4.2, 4.3, 4.2,
                 -2.5, -2.6,  -2.4]
            vf = interp1d(x, v, kind='cubic')
            self.parameter = vf

        self.instrument = instrument
        print("{} connected.".format(instrument))

    def trigger(self):
        self.time = 0.0
        print("triggered at {}".format(datetime.datetime.now()))

    def voltage(self, t):
        inst_type = self.INSTRUMENTS.index(self.instrument)
        if inst_type == 3:
            voltage = self.parameter(t)
        else:
            voltage = self.parameter[0] + t * self.parameter[1]
        return voltage

    def measured(self, t):
        volts = self.voltage(t)
        volts[:] = [x + random.gauss(0.0, 16) * self.Q for x in volts]
        return np.clip(volts, self.REF_LOW, self.REF_HIGH)

    def quantisize(self, t):
        volts = self.measured(t)
        volts[:] = [math.floor((v - self.REF_LOW) / self.Q) for v in volts]
        return volts

    def next_reading(self):
        # ensure DELTA_T seconds between readings
        delta = time.time() - self.last_reading
        delay = max(0.0, self.DELTA_T-delta)
        if self.wait and delay>0:
            time.sleep(delay)
        self.last_reading = time.time()

        # increment time and create a reading
        self.time = self.time + self.DELTA_T
        volts = self.voltage(self.time)
        volts += random.gauss(0,0.25)

        if volts < self.REF_LOW:
            volts = self.REF_LOW
        if volts > self.REF_HIGH:
            volts = self.REF_HIGH
        volts = int(math.floor((volts - self.REF_LOW) / self.Q))
        return datetime.datetime.now(), volts
