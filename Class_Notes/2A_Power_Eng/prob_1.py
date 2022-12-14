# Example 1-1 in Electric Machinery Fundamentals

import numpy as np

N = 200 # turns
curr =  1 # amps
mu_r = 2500 # relative permeability
mu_o = np.pi * 4e-7 # permeability of vacuum
f = N*curr # magnetomotive force
mu = mu_r * mu_o # total permeability
A_1 = 15e-2 * 10e-2 # m^2
l_1 = (5 + 30 + 15 + 30 + 15 + 30 + 5)*1e-2 # m
print("l1 = " + str(l_1))
A_2 = 10e-2 * 10e-2 # m^2
l_2 = (7.5 + 30 + 7.5)*1e-2 # m
reluctance_1 = l_1 / (A_1 * mu)
print("r1 = " + str(reluctance_1))
reluctance_2 = l_2 / (A_2 * mu)
print("r2 = " + str(reluctance_2))
reluctance_total = reluctance_1 + reluctance_2
# f = φr
flux = f/reluctance_total
print("flux = " + str(flux))
