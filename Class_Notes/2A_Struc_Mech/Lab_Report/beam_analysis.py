"""
Euler beam analysis on a composite section

goals:
- plot 150N bending moment strain vs height 
- plot actual strain vs height on same graph
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import matplotlib

matplotlib.style.use('seaborn-v0_8-paper')

unbondeddf = pd.read_excel("unbonded_beam_values.xlsx")
bondeddf = pd.read_excel("bonded_beam_values.xlsx")

# print(unbondeddf["Weight"])
# print(bondeddf["Weight"])


ubrow = unbondeddf.loc[unbondeddf["Weight"]==150]
brow = bondeddf.loc[bondeddf["Weight"]==150]

# print(brow.keys())

ubgauge = [ubrow.at[4,"Gauge 1"],ubrow.at[4,"Gauge 2 "],ubrow.at[4,"Gauge 3 "],ubrow.at[4,"Gauge 4 "],ubrow.at[4,"Gauge 5 "],ubrow.at[4,"Gauge 6"]]
bgauge = [brow.at[4,"Gauge 1 "],brow.at[4,"Gauge 2"],brow.at[4,"Gauge 3 "],brow.at[4,"Gauge 4 "],brow.at[4,"Gauge 5 "],brow.at[4,"Gauge 6 "]]

gauge_ys = [0, 5, 5, 43-17.5, 43-17.5, 43]

print(ubgauge)
print(bgauge)


F = 9 * 150
M = 212.5 * F *1e-3 # kilonewton-millimeters
E = 200 # kN / mm^2
centroid = (30 * 5 * 2.5 + 38 * 30 * 7/20 * 24)/(30 * 5 + 38 * 30 * 7/20) # mm
I = 30*(5**3)/12 + 30*5*((centroid-2.5)**2) + (38**3 * 30*7/20)/12 + (38*30*7/20)*((24-centroid)**2)# mm^4

print(f"I = {I}")

kappa = M/(E*I) # 1/millimeters

def strain(y):
    return kappa * y


print(f"centroid = {centroid} ")

y = np.linspace(0, 43, 1000)

predstrain = [1e6 * strain(yval - centroid) for yval in y]

predstraingauges = [1e6*strain(yval - centroid) for yval in gauge_ys]

print(predstraingauges)

fig,ax = plt.subplots()

ax.plot(predstrain, y, color='C3', label='Strain Prediction')
ax.scatter(ubgauge, gauge_ys, marker='s', color='C1', label='Unbonded Beam')
ax.scatter(bgauge, gauge_ys, marker='o', color='C2', label='Bonded Beam')

annotations = ["G" + str(i) for i in range(1,7)]

ubann = ubgauge.copy()
# ubann[2] = -250
ubannys = gauge_ys.copy()
ubann[4] = 0
ubann[3] = 60-16
bannys = gauge_ys.copy()
bannys[2-1]=5
bannys[3-1]=7
bannys[4-1]=25
bannys[5-1]=27

for i, label in enumerate(annotations):
    ax.annotate(label, (ubann[i], ubannys[i]) )
    ax.annotate(label, (bgauge[i], bannys[i]) )


ax.set_yticks([0,5,10,15, 18.22,20,25,30,35,40,43])

ax.hlines(18.22,ax.set_xlim()[0], ax.set_xlim()[1], linestyle='--', color="gray")

ax.set_ylabel("Y distance (mm)")

ax.set_xlabel("Strain (με)")

ax.legend()

ax.grid()

plt.gca().invert_yaxis()

plt.savefig("Beam_Figure_1.png")