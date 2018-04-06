import matplotlib.pyplot as plt
import matplotlib.patches as patches
import csv
import numpy as np
import operator
import pandas as pd

def plot_rect(data, delta=0.4):
    """data is a dictionary, {"Label":(low,hi), ... }
    return a drawing that you can manipulate, show, save etc"""

    yspan = len(data)
    yplaces = [.5+i for i in range(yspan)]
    ylabels = []

    b = data.items()
    b.sort(key=lambda x: x[1][1], reverse=True)
    for i in b:
        ylabels.append(i[0])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_yticks(yplaces)
    ax.set_yticklabels(ylabels, fontsize= 8)
    ax.set_ylim((0,yspan))
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    plt.xscale('log')

    # later we'll need the min and max in the union of intervals
    lx = []
    ly = []
    hx = []
    hy = []

    low_min, low_max, low_avg, high_min, high_max, high_avg = data[ylabels[0]]

    for pos, label in zip(yplaces,ylabels):
        Low_min, Low_max, Low_Average, High_min, High_max, High_Average = data[label]
        ax.add_patch(patches.Rectangle((Low_min,(pos-delta/2.0)-0.18),Low_max-Low_min,delta,facecolor='#d7d9db', edgecolor='#6d7378'))
        ax.text(Low_max+Low_Average/6,(pos-delta/2.0)-0.18, str(np.round(Low_Average,1)), fontsize=7)
        lx.append(Low_Average)
        ly.append(pos - delta / 2.0)


        if High_Average > 0.0:
            ax.add_patch(patches.Rectangle((High_min, (pos - delta / 2.0) - 0.18), High_max - High_min, delta, facecolor='#d7d9db',edgecolor='#6d7378'))
            ax.text(High_Average+High_Average*0.5, (pos - delta / 2.0) - 0.18, str(np.round(High_Average, 1)), fontsize=7)
            hx.append(High_Average)
            hy.append(pos - delta / 2.0)

    # calcalate average and plot average
    average = np.average(lx)
    stdev = np.std(lx)
    plt.axvline(x=average, color = '#ff4d4d')
    ax.text(average + average / 2, len(data)-1, "Mean: " + str(np.round(average, 1)) + " +/- " + str(np.round(stdev,1)), fontsize=11, color = '#ff4d4d')

    ax.plot((low_min,low_max),(0,0))
    ax.plot(lx, ly, marker='s', color = '#737373', linewidth = 0)
    ax.plot(hx, hy, marker='s', color='#737373', linewidth=0)


    # now get the limits as automatically computed
    xmin, xmax = ax.get_xlim()
    # and use them to draw the hlines in your example
    ax.grid(False)

    # eventually return what we have done
    return ax


# this is the main script, note that we have imported pyplot as plt
rangedata = {}
f = open('csvData.csv', 'rb')
reader = csv.reader(f)
for row in reader:
    i = row
    Name = str(i[0])
    Low_min = float(i[1])
    Lox_max = float(i[3])
    Low_Average = float(i[2])
    Max_min = 0
    Max_max = 0
    Max_Average = 0
    try:
        Max_min = float(i[4])
    except:
        donothing = None
    try:
        Max_max = float(i[6])
    except:
        donothing = None
    try:
        Max_Average = float(i[5])
    except:
        donothing = None

    rangedata[Name] = (Low_min, Lox_max, Low_Average, Max_min, Max_max, Max_Average)
f.close()

print rangedata


# call the function and give its result a name
ax = plot_rect(rangedata)
# so that we can further manipulate it using the `axes` methods, e.g.
ax.set_xlabel('Log of Particle Diameter [um]')
# finally save or show what we have
plt.show()