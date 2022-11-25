"""
Truss Analysis in Python

Goals: 

- find a linear regression for strain against slider value
- plot this regression with matplotlib

"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import matplotlib

df = pd.read_csv("D:\\MarkdownMaster\\Class_Notes\\2A_Struc_Mech\\TRUSS_SNAPSHOTS_22112022.csv")


df["slideradj"] = [0, 3, 6, 9, 12]
df["slider"] = [3,6,9,12,15]

# m1 = np.polyfit(df["G1"], df["slider"], 1)

res1 = sm.OLS(df["G1"], df["slideradj"]).fit()
res2 = sm.OLS(df["G2"], df["slideradj"]).fit()
res3 = sm.OLS(df["G3"], df["slideradj"]).fit()
res4 = sm.OLS(df["G4"], df["slideradj"]).fit()
res5 = sm.OLS(df["G5"], df["slideradj"]).fit()
res6 = sm.OLS(df["G6"], df["slideradj"]).fit()

reses = [res1, res2, res3, res4, res5, res6]

# print(dir(res1))

paramses = []
rsquaredses = []


# print(res1.summary())
for result in reses: 
    paramses.append(result.params)
    rsquaredses.append(result.rsquared)
    # print(result.params)


print(paramses)
print(rsquaredses)

resdf = pd.DataFrame({
    "Gauge": ["G1", "G2", "G3", "G4", "G5", "G6"],
    "Parameters": paramses,
    "R2 Vals": rsquaredses,
})

resdf.to_csv("D:\\MarkdownMaster\\Class_Notes\\2A_Struc_Mech\\Truss_Analysis_Results_2.csv")

fig,ax = plt.subplots()

matplotlib.style.use('seaborn-v0_8-paper')

ax.scatter(df["slider"], df["G1"], label="G1", color='C1', marker="o")
ax.scatter(df["slider"], df["G2"], label="G2", color='C2', marker="^")
ax.scatter(df["slider"], df["G3"], label="G3", color='C3', marker="s")
ax.scatter(df["slider"], df["G4"], label="G4", color='C4', marker="p")
ax.scatter(df["slider"], df["G5"], label="G5", color='C5', marker="h")
ax.scatter(df["slider"], df["G6"], label="G6", color='C6', marker="x")

for i in range(0,6):
    ax.plot([3,15], [3, 12*paramses[i]],'--', color='C' + str(i+1), label='G' + str(i+1))

ax.set_xlabel("Slider value")
ax.set_ylabel("Strain (με)")
ax.set_xticks([3,6,9,12,15])
ax.grid()

handle1 = matplotlib.lines.Line2D([],[],linestyle='--',color='C1',marker='o',markersize=7,label="G1")
handle2 = matplotlib.lines.Line2D([],[],linestyle='--',color='C2',marker='^',markersize=7,label="G2")
handle3 = matplotlib.lines.Line2D([],[],linestyle='--',color='C3',marker='s',markersize=7,label="G3")
handle4 = matplotlib.lines.Line2D([],[],linestyle='--',color='C4',marker='p',markersize=7,label="G4")
handle5 = matplotlib.lines.Line2D([],[],linestyle='--',color='C5',marker='h',markersize=7,label="G5")
handle6 = matplotlib.lines.Line2D([],[],linestyle='--',color='C6',marker='X',markersize=7,label="G6")

handles = [handle1, handle2, handle3, handle4, handle5, handle6]

ax.legend(handles=handles)

# print(df)
plt.show()