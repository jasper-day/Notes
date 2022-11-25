import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

matplotlib.style.use('seaborn-v0_8-paper')

diam = 10 # mm
length = 280 # mm
J = np.pi * (diam/2)**4 / 2 # mm^4
# print(J)

weight = [0.9, 1.8]

steel_d = [0.30, 0.58]
al_d = [0.71, 1.39]
correction = [0.08, 0.16]

steel_dc = [steel_d[i] - correction[i] for i in [0,1]]
al_dc = [al_d[i] - correction[i] for i in [0,1]]

# print(steel_dc)
# print(al_dc)

def T(mass): # kN-mm
    return 100*mass*9.81*1e-3

def phi(d):
    return d/55

print("Torsion values:")

torsions = [T(val) for val in weight]

print("phi values:")

steel_phi = [phi(val) for val in steel_dc]
al_phi = [phi(val) for val in al_dc]

# phi = TL / GJ
# G = TL / phi J   kN-mm * mm / rad * mm^4 = kn/mm^2 = GPa

def G(t, phi, l=280, j=J):
    return t * l / (phi * j)

print("G values:")

G_steel = [G(T(weight[i]), phi(steel_dc[i])) for i in [0,1]]
G_al = [G(T(weight[i]), phi(al_dc[i])) for i in [0,1]]

print(f"steel average {np.average(G_steel)} and s.d. {np.std(G_steel)}")
print(f"al average {np.average(G_al)} and s.d. {np.std(G_al)}")

fig,ax = plt.subplots()

ax.scatter(torsions, steel_phi, marker='s', color='C1', label='Steel')
ax.scatter(torsions, al_phi, marker='o', color='C2', label='Aluminum')

res_steel = sm.OLS(steel_phi, torsions).fit()
res_al = sm.OLS(al_phi, torsions).fit()

param_steel = res_steel.params
r_steel = res_steel.rsquared
param_al = res_al.params
r_al = res_al.rsquared

print(res_steel.summary())
print(res_al.summary())

print("steel r2" + str(r_steel))
print("al r2" + str(r_al))

ax.plot([0,1.8], [0,1.8*param_steel], linestyle='--', color='C1',alpha=0.5)
ax.plot([0,1.8], [0,1.8*param_al], linestyle='--', color='C2',alpha=0.5)

ax.set_xlabel("Torsion (kN-mm)")
ax.set_ylabel("Rotation (rad)")

ax.legend()

ax.grid()

ax.set_xticks(np.linspace(0,2.5,11))
ax.set_yticks(np.linspace(0,0.025,11))

plt.show()

