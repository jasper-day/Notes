import numpy as np
import plotly.express as px
import pandas as pd
import pint

ureg = pint.UnitRegistry()

t1data = pd.read_csv('gyroscope.csv')
t2data = pd.read_csv('gyroscopet2.csv')

Q_ = ureg.Quantity

print(t1data)
print(t2data)

# capital Omega = gyroscope rotation speed
# lowercase omega = precession speed

# t1 data

tconst = 2500 * ureg.rpm
tconst_err = 60 * ureg.rpm

r = t1data['r'].to_numpy() * ureg.mm # distance to weight

g = 9.81 * Q_('m/s^2')
M = 0.0656 * ureg.kg

torque = r * M * g

r_err = t1data['e_r'].to_numpy() * ureg.mm
r_err_partial = r_err / r

torque_err = torque * r_err_partial

