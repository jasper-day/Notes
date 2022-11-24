
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

matplotlib.style.use('seaborn-v0_8-paper')

pbar = 20 # bar
p = 0.002 # kN/mm^2
r = 36.25 # mm
t = 2.5 # mm

E = 70 # kN/mm^2
nu = 0.33 #poisson

sigmah = p*r/t
sigmal = p*r/(2*t)

print(sigmah)
print(sigmal)

open_epsh = sigmah/E * 1e6
open_epsl = -nu*sigmah/E * 1e6

clo_epsh = (sigmah/E - nu*sigmal/E) * 1e6
clo_epsl = (sigmal/E - nu*sigmah/E) * 1e6

print(f"Open epsh {open_epsh} open epsl {open_epsl} closed epsh {clo_epsh} closed epsl {clo_epsl}")

theta = np.linspace(0, np.pi, 1000)

mohr_open_x = sigmah/2 + sigmah/2 * np.cos(2 * theta)
mohr_open_y = sigmah/2 * np.sin(2 * theta)

mohr_closed_x = (sigmah+sigmal)/2 + (sigmah-sigmal)/2 * np.cos(2 * theta)
mohr_closed_y = (sigmah-sigmal)/2 * np.sin(2 * theta)

fig, ax = plt.subplots()

ax.plot(mohr_open_x, mohr_open_y, color='C1', label='Open condition')
ax.plot(mohr_closed_x, mohr_closed_y, color='C2', label='Closed condition')

ax.hlines(0,ax.set_xlim()[0], ax.set_xlim()[1], color='black')
ax.vlines(0,ax.set_ylim()[0], ax.set_ylim()[1], color='black')

ax.set_aspect('equal')

ax.set_xlabel(r'$\sigma$ (kN/mm$^2$)')
ax.set_ylabel(r'$\tau$ (kN/mm$^2$)')

ax.minorticks_on()

ax.legend(loc="lower right")

ax.grid()

plt.show()