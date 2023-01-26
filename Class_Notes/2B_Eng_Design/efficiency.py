import numpy as np
import matplotlib.pyplot as plt


print("Python program to determine the efficiency of a paper crane structure (TED 2023)")

P = input("Enter the load carrying capacity of the crane in Newtons: ")
R = input("Enter the number of cotton reels used in the design: ")
s = input("Enter the number of paper sheets used in the design: ")
A = input("Enter the number of axles used in the design: ")

eff = P**(3/(R + 1)) * (np.sqrt(40 - s)) + 100/(A + 1)

print(f"The crane efficiency is {eff}")