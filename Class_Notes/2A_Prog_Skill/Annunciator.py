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
import matplotlib.pyplot as plt; plt.ion
import numpy as np 
import pandas as pd

# Data Acquisition setup 

my_daq = DAQ(matric = 's2265891', user = 'Jasper Day')

my_daq.connect('coursework')

my_daq.trigger()

df = pd.DataFrame({"volts":[]})

ax = df.plot.line()

while True:
    cur_time, cur_volts = my_daq.next_reading()
    df.loc[cur_time] = cur_volts
    df.plot.line(ax = ax, reuse_plot=True)
    print(f"The time is {cur_time} and the voltage is {cur_volts}")
    plt.pause(0.001)
    plt.show()