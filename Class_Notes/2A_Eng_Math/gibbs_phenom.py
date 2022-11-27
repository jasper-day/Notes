"""
Code showing off the "gibbs phenomenon" of overshoot around the corners of a discontinuity.
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpt

L = 10 
N = 1024
dx = L / N

x = np.linspace(0,L,N)

f = np.zeros_like(x)

f[int(N/4):int(3*N/4)] = 1

A = [0]
B = [0]

A0 = np.sum(f) / N
fFS = np.ones_like(x) * A0

fig,ax = plt.subplots()
colorgradient = np.linspace(0,1,20)
cmap = mpt.cm.get_cmap("tab10")
colors = cmap.colors
ax.set_prop_cycle(color=colors)

# ax.plot(fFS)


for k in range(1,int(N/2)):
    # take inner product of sin function with frequency k 
    A.append( np.inner(f, np.cos(x*k*2*np.pi/L))*dx*2/L)
    B.append( np.inner(f, np.sin(x*k*2*np.pi/L))*dx*2/L)

    fFS += A[k] * np.cos(x * k * 2*np.pi/L) + B[k] * np.sin(x * k * 2*np.pi/L)

ax.plot(fFS)
ax.plot(f)
plt.show()

