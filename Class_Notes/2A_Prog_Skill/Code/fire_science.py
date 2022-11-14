import matplotlib.pyplot as plt
import math
import time
import numpy as np

T_a = 20
mass = 6200
cp = 0.94
h = 25
area = (6.4E-3*(0.2-9.6E-3-9.6E-3))*2 + ((0.2-9.6E-3-9.6E-3)*3)*2
sigma = 5.67E-8
emissivity = 0.7
rho = 475
delta_t = 1
start_T_b = 20
n_iterations = 1000
timing = np.linspace(0,n_iterations,n_iterations)

count = 0
failtemp = 550 # °C



def T_g(time): # gas phase temperature as a function of time
    return 20+(345*math.log10(0.133*time+1))
    
def next_val_T_b(time, prev_value):
    Ein = (h * area * (T_g(time) - prev_value))
    Eout = emissivity*sigma*area*((273 + prev_value)**4 - (273 + T_a)**4)
    return prev_value + delta_t / (mass * cp) * (Ein - Eout)

T_b = [start_T_b]

for i in range(1, n_iterations):
    T_b.append(next_val_T_b(i, T_b[i - 1]))

plt.plot(np.arange(0,1000,1), T_b)
plt.plot([0,1000],[550,550],'--')
plt.show()

# time = list(range(0, n_iterations))*delta_t
# for i in range(1, n_iterations):
#     T_b.append(
#         T_b[i-1] + delta_t/(mass*cp) *
#             (h*area*(Tg-T_b[i-1])
#              - emissivity*sigma*area*((273+T_b[i-1])**4 - (273+T_a)**4))) #
#     if T_b[i-1] >= failtemp:
#         print('reached first if')
#         q = i
#         if count == 0:
#             print('reached this point')
#             threshold = T_b[i-1]
#             count += 1
#     else:
#         pass
        

# max_temp = max(T_b)
# print(threshold)
# print(q)
# print('The max temperature is ' + str(round(max_temp)) + '°C')


# fig,ax1 = plt.subplots()
# ax1.plot([0,max(time)],[550,550],'--',color='red', label='Beam failure temperature')
# ax1.plot(timing, T_b)
# ax1.set_xlabel('Time, s')
# ax1.set_ylabel('Temperature, °C')
# ax1.legend()
# plt.rcParams["legend.loc"] = 'lower right'
# ax1.set_xlim(0,600)
# ax1.set_ylim(0,800)
# plt.show()