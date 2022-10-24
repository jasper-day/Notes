# ++============================================++
# || Programming for Engineers: Toucan Crossing ||
# ||-------------+------------+-----------------||
# || Jasper Day  |  S2265891  |  2022/10/20     ||
# ++============================================++
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# size of the crowd
N = 100

def gen_data():
    """ init position and speed of each people """
    x = y = np.zeros(N)
    theta = np.random.random(N) * 360 / (2 * np.pi)
    v0 = 0.1
    vx, vy = v0 * np.cos(theta), v0 * np.sin(theta)
    return np.column_stack([x, y, vx, vy])

def init():
    pathcol.set_offsets([[], []])
    return pathcol,

import numpy as np

class TrafficObject:
     pos2 = np.array([])