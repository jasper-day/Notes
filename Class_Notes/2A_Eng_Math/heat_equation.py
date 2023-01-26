import matplotlib as mpt
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import sys

delta_x = 0.01

x = np.arange(0,1,delta_x)

square = lambda x: 0 if np.floor(4*x) % 4 in (0,3) else 1
squares = lambda x: 0 if np.floor(11*x) % 2 == 0 else 1
hat = lambda x: 1 - 2 * np.abs(x - 0.5)

args = sys.argv
try:
    if args[1] == "square":
        chosen_fun = square
    elif args[1] == "squares":
        chosen_fun = squares
    elif args[1] == "hat":
        chosen_fun = hat
    else:
        chosen_fun = eval(args[1])
except:
    chosen_fun = lambda x: 1


broadcast = lambda op, x: [op(i) for i in x]

# plt.plot(x, broadcast(square,x))
# plt.plot(x, broadcast(squares,x))
# plt.plot(x, broadcast(hat,x))

def A(n, x, f_x):
    const = 2/np.sinh(np.pi * n)
    integral = np.dot(f_x, np.sin(np.pi * n * x)) * delta_x
    return const * integral

def u(X,Y,num_coeff, boundary_fun, x=x):
    Aspef = lambda n: A(n, x, broadcast(boundary_fun, x))
    F = lambda X, n: np.sinh(np.pi * n * X)
    G = lambda Y, n: np.sin(np.pi * n * Y)
    return np.sum([Aspef(n) * F(X, n) * G(Y, n) for n in range(1, num_coeff)], 0)

X, Y = np.meshgrid(x,x)

fig, ax = plt.subplots(subplot_kw = {"projection": "3d"})

ax.plot_surface(X, Y, u(X,Y, 202, chosen_fun), cmap=cm.coolwarm)

plt.show(
    )
