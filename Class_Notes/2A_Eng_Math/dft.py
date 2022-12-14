import matplotlib as mpt
import matplotlib.pyplot as plt
import numpy as np

n = 512

w = np.exp(-1j * 2 * np.pi/n)

J, K = np.meshgrid(np.arange(n), np.arange(n))
DFT = np.power(w, J*K)
DFT = np.real(DFT)

plt.imshow(DFT)
plt.show()  