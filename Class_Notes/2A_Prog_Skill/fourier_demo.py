import pandas as pd
import os, sys
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10,6]
plt.rcParams.update({'font.size': 18})
plt.style.use('seaborn')

## Create synthetic signal
dt = 0.001
t = np.arange(0, 1, dt)
signal = np.sin(2*np.pi*10*t) + np.sin(2*np.pi*20*t) #composite signal array 1000 values
signal_clean = signal #copy for later comparison
signal = signal + 2.5 * np.random.randn(len(t))
minsignal, maxsignal = signal.min(), signal.max()

## Compute Fourier Transform
n = len(t)
fhat = np.fft.fft(signal, n) #computes the fft
psd = fhat * np.conj(fhat)/n
freq = (1/(dt*n)) * np.arange(n) #frequency array
idxs_half = np.arange(1, np.floor(n/2), dtype=np.int32) #first half index

fig,ax = plt.subplots(2)

datax = ax[0]
fourax = ax[1]

datax.plot(signal, color="C1", label="data")

fourax.plot(psd, color="C2", label="frequencies")

plt.show()