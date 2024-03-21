import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MinuteLocator, SecondLocator
import numpy as np
import pandas as pd
import datetime as dt
import io
import matplotlib.patches as mpatches


#Plot function
def timelines(y, xstart, xstop, color='b'):
    """Plot timelines at y from xstart to xstop with given color."""   
    plt.hlines(y, xstart, xstop, color, lw=4)
    plt.vlines(xstart, y+0.03, y-0.03, color, lw=2)
    plt.vlines(xstop, y+0.03, y-0.03, color, lw=2)

y_vals = [40, 45, 50, 55, 60]
yes = [[0.249, 0.425], [0.374, 0.525], [0.449, 0.55], [0.524, 0.6], [0.574, 0.700]]
no = [[0.799, 0.875], [0.849, 0.9], [0.874, 0.9], [0.874, 0.925], [0.899, 0.950]]
difference = [0.941, 0.764, 0.764, 0.823, 0.647]
# 40
# 27 73
# ConfidenceInterval(low=0.249, high=0.425)
# ConfidenceInterval(low=0.799, high=0.875)
# (17, 17, 0.9411764705882353, 0.8682504911471942, 1)

# 45
# 41 59
# ConfidenceInterval(low=0.374, high=0.525)
# ConfidenceInterval(low=0.849, high=0.9)
# (17, 17, 0.7647058823529411, 0.8682504911471942, 1)

# 50
# 46 54
# ConfidenceInterval(low=0.449, high=0.55)
# ConfidenceInterval(low=0.874, high=0.9)
# (17, 17, 0.7647058823529411, 0.8682504911471942, 1)

# 55
# 59 41
# ConfidenceInterval(low=0.524, high=0.6)
# ConfidenceInterval(low=0.874, high=0.925)
# (17, 17, 0.8235294117647058, 0.8682504911471942, 1)

# 60
# 75 25
# ConfidenceInterval(low=0.5740000000000001, high=0.7000000000000001)
# ConfidenceInterval(low=0.899, high=0.9500000000000001)
# (17, 17, 0.6470588235294118, 0.8682504911471942, 1)

yes_y = []
yes_x_start = []
yes_x_end = []

no_y = []
no_x_start = []
no_x_end = []

for x in range(0, len(y_vals)):
    yes_y.append(y_vals[x]-0.5)
    no_y.append(y_vals[x]+0.5)

    yes_x_start.append(yes[x][0])
    yes_x_end.append(yes[x][1])

    no_x_start.append(no[x][0])
    no_x_end.append(no[x][1])

    plt.annotate(difference[x], xy = (yes[x][1] - 0.05 + (no[x][0]-yes[x][1])/2, y_vals[x]-0.5))

yes_y = np.array(yes_y)
yes_x_start = np.array(yes_x_start)
yes_x_end = np.array(yes_x_end)

no_y = np.array(no_y)
no_x_start = np.array(no_x_start)
no_x_end = np.array(no_x_end)

#Plot ok tl black    
timelines(yes_y, yes_x_start, yes_x_end, 'g')
#Plot fail tl red
timelines(no_y, no_x_start, no_x_end, 'r')

#Setup the plot
# ax = plt.gca()
# ax.xaxis_date()
# myFmt = DateFormatter('%H:%M:%S')
# ax.xaxis.set_major_formatter(myFmt)
# ax.xaxis.set_major_locator(SecondLocator(interval=20)) # used to be SecondLocator(0, interval=20)

# #To adjust the xlimits a timedelta is needed.
# delta = (stop.max() - start.min())/10
plt.yticks(y_vals)
# plt.ylim(0,1)
# plt.xlim(start.min()-delta, stop.max()+delta)
plt.xlabel("Error Rate")
plt.ylabel("Noise")
yes_patch = mpatches.Patch(color='green', label='Noise < X')
no_patch = mpatches.Patch(color='red', label='Noise >= X')
plt.legend(handles=[yes_patch, no_patch], loc="upper left")
plt.show()