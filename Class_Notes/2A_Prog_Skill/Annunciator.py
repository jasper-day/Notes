"""
+============+==========================+
|  Title     |  Annunciator  Project    |   
+------------+--------------------------+
|  Author    |  Jasper Day              | 
+------------+--------------------------+
|  Date      |  2022.11.17              | 
+============+==========================+

Goal: Implement an annunciator panel in Python using your blinkstick and the 
scada.py library.
- A green light should come on when the sensor is above 4.27V
- A red light should come on when the sensor is below -2.56V
- No lights must show between -2.56 and 4.27V
- Lights must not flicker

"""

from scada import DAQ
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np 
import pandas as pd

REF_HIGH = +5.0 # high voltage limit on sensor
REF_LOW = -5.0  # low voltage limit on sensor
BITS = 10       # number of bits used to encode the signal
DELTA_T = 0.5   # sample period (s)
V_HIGH = 4.27   # highest permissible voltage
V_LOW = -2.56   # lowest permissible voltage

style.use("fast")

# Data Acquisition setup 

my_daq = DAQ(matric = 's2265891', user = 'Jasper Day')
my_daq.connect('coursework')
my_daq.trigger()

# The Annunciator class implements a digital display of the current voltage 
# readout, as well as interfacing with the blinkstick.

class Annunciator:
    def __init__(self, ax, daq):
        self.ax = ax
        self.daq = daq
        self.voltages = []
        self.clean_voltages = []
    
    def update(self, frame):
        self.clean_voltage()

        self.ax.clear()

        self.ax.plot(self.voltages[-120:], color="blue", label="Raw")
        self.ax.plot(self.clean_voltages[-120:], color="green", label="Smoothed")

        self.ax.set_ylim(REF_LOW - 0.5, REF_HIGH + 0.5)

        self.ax.set_ylabel("Voltage")
        self.ax.set_title("Voltage vs. Time for DAQ")

        # Graph upper and lower limits for voltage

        self.ax.axhline(y = V_LOW, color="red", linestyle="--")
        self.ax.axhline(y = V_HIGH, color="red", linestyle="--")

        self.ax.fill_between(x = self.ax.set_xlim(), y1=V_LOW,y2=V_HIGH, color="green", hatch='/', alpha=0.2)
        self.ax.fill_between(x = self.ax.set_xlim(), y1=REF_LOW,y2=V_LOW, color="red", hatch='/', alpha=0.2)
        self.ax.fill_between(x = self.ax.set_xlim(), y1=V_HIGH,y2=REF_HIGH, color="red", hatch='/', alpha=0.2)
        
        
        self.ax.legend()

    def read_voltage(self):
        cur_time, cur_volts = self.daq.next_reading()
        Q = (REF_HIGH - REF_LOW) / 2 ** BITS
        cur_volts_converted = cur_volts * Q + REF_LOW
        print(f"The time is {cur_time} and the voltage is {cur_volts_converted}")
        self.voltages.append(cur_volts_converted)
        yield 1
    
    def clean_voltage(self):
        self.clean_voltages.append(np.average(self.voltages[-10:]))

fig, ax = plt.subplots()
annunciator = Annunciator(ax, my_daq)

ani = animation.FuncAnimation(fig, annunciator.update, annunciator.read_voltage, interval=50)

plt.show()

# volts = []
# x_time = []

# style.use("fivethirtyeight")

# fig, ax = plt.subplots()
# ln, = ax.plot(x_time, volts)

# def init():
#     ax.set_ylim(-4.5,4.5)   
#     ax.set_xlim(0,100)
#     return ln,

# def update(cur_volts):
#     global volts
#     volts.append(cur_volts)
#     # x_time = x_time[-50,:]

#     ln.set_data(x_time, volts)
#     return ln,

# def generator(daq):
#     cur_time, cur_volts = my_daq.next_reading()
#     return cur_volts


# ani = animation.FuncAnimation(fig, update, generator, interval=5, init_func=init, blit=True)

# plt.show()

# # while True:
# #     cur_time, cur_volts = my_daq.next_reading()
# #     df.loc[cur_time] = cur_volts
# #     print(f"The time is {cur_time} and the voltage is {cur_volts}")