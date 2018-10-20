import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import csv
import numpy as np
import operator
import pandas as pd

def plot_rect(data):
    delta = 0.4
    yspan = len(data)
    yplaces = [.5+i for i in range(yspan)]
    ylabels = []

    # sort the list of soil types by average diameter
    b = data.items()
    b.sort(key=lambda x: x[1][3], reverse=True)
    for i in b:
        ylabels.append(i[0])

    print b

    fig = plt.figure(dpi=120)
    ax = fig.add_subplot(111)
    plt.title('Soil Particle Size Distribution Around the World')

    # set up the plot
    ax.set_yticks(yplaces)
    ax.set_yticklabels(ylabels, fontsize= 8)
    ax.set_ylim((0,yspan))
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    plt.xscale('log')

    # list of values for all of soil samples
    # general list
    lx = []
    ly = []

    # for davids data
    david_lx = []
    david_ly = []

    # for mean calcuated from range
    m_lx = []
    m_ly = []


    # for average reported in literature
    a_lx = []
    a_ly = []

    # for distribution reported in literature
    d_lx = []
    d_ly = []
    standard = []

    def writePointToList(pos, delta, value, type):

        if type == "Mean from Reported Range":
            m_ly.append(pos - delta / 2.0)
            m_lx.append(value)

        if type == "Reported Average":
            a_ly.append(pos - delta / 2.0)
            a_lx.append(value)

        if type == "Mean from Reported Distribution":
            d_ly.append(pos - delta / 2.0)
            d_lx.append(value)


    max, low_min, low_max, low_avg, high_min, high_max, high_avg, top_min, top_max, top_avg, method, david, valuetype = data[ylabels[0]]

    # add all of the soil samples to the plot - make a rectangle for each sample
    for pos, label in zip(yplaces,ylabels):

        lbl = str(label)
        if lbl.startswith("PT-") or lbl.startswith("ASTM"):
            Max, Low_min, Low_max, Low_Average, High_min, High_max, High_Average, Top_min, Top_max, Top_Average, Method, David, ValueType = data[label]
            Low_Average = np.round(Low_Average,1)
            ax.add_patch(
                patches.Rectangle((Low_min, (pos - delta / 2.0) - 0.18), Low_max - Low_min, delta, facecolor='#00e6ac',
                                  edgecolor='#00b386'))
            ax.text(Low_max + Low_Average / 4, (pos - delta / 2.0) - 0.18, str(np.round(Low_Average, 1))
                    # +" - "+str(label)
                    , fontsize=7, color = '#004d39')


            d_lx.append(Low_Average)
            d_ly.append(pos - delta / 2.0)
            standard.append(low_avg)



        else:
            Max, Low_min, Low_max, Low_Average, High_min, High_max, High_Average, Top_min, Top_max, Top_Average, Method, Source, ValueType = data[label]

            Low_Average = np.round(Low_Average, 1)
            High_Average = np.round(High_Average, 1)
            Top_Average = np.round(Top_Average, 1)

            # Differentiate between Literature search, Leo and David
            # if Source == "David":
            #     ly.append(pos - delta / 2.0)
            #     lx.append(Low_Average)
            #     ax.add_patch(patches.Rectangle((Low_min,(pos-delta/2.0)-0.18),Low_max-Low_min,delta,facecolor='#d7d9db', edgecolor='#6d7378'))
            #     ax.text(Low_max+Low_Average/6,(pos-delta/2.0)-0.18, str(np.round(Low_Average,2)), fontsize=7)
            #     david_lx.append(Low_Average)
            #     david_ly.append(pos - delta / 2.0)
            #
            #     if High_Average > 0.0:
            #
            #         ax.add_patch(patches.Rectangle((High_min, (pos - delta / 2.0) - 0.18), High_max - High_min, delta, facecolor='#d7d9db', edgecolor='#6d7378'))
            #         ax.text(High_Average+High_Average*0.5, (pos - delta / 2.0) - 0.18, str(np.round(High_Average, 1)), fontsize=7)
            #         david_lx.append(High_Average)
            #         david_ly.append(pos - delta / 2.0)
            #
            #     if Top_Average > 0.0:
            #         ax.add_patch(patches.Rectangle((Top_min, (pos - delta / 2.0) - 0.18), Top_max - Top_min, delta, facecolor='#d7d9db', edgecolor='#6d7378'))
            #         ax.text(Top_Average + Top_Average*0.5, (pos - delta / 2.0) - 0.18, str(np.round(Top_Average, 1)), fontsize=7)
            #         david_lx.append(Top_Average)
            #         david_ly.append(pos - delta / 2.0)
            #
            if Source == "Leo":
                pass
            #     ly.append(pos - delta / 2.0)
            #     lx.append(Low_Average)
            #     ax.add_patch(patches.Rectangle((Low_min,(pos-delta/2.0)-0.18),Low_max-Low_min,delta,facecolor='#E57A63', edgecolor='#ba6223'))
            #     ax.text(Low_max+Low_Average/6,(pos-delta/2.0)-0.18, str(np.round(Low_Average,2)), fontsize=7)
            #     david_lx.append(Low_Average)
            #     david_ly.append(pos - delta / 2.0)
            #
            #     if High_Average > 0.0:
            #
            #         ax.add_patch(patches.Rectangle((High_min, (pos - delta / 2.0) - 0.18), High_max - High_min, delta, facecolor='#E57A63',edgecolor='#ba6223'))
            #         ax.text(High_Average+High_Average*0.5, (pos - delta / 2.0) - 0.18, str(np.round(High_Average, 1)), fontsize=7)
            #         david_lx.append(High_Average)
            #         david_ly.append(pos - delta / 2.0)
            #
            #     if Top_Average > 0.0:
            #         ax.add_patch(patches.Rectangle((Top_min, (pos - delta / 2.0) - 0.18), Top_max - Top_min, delta, facecolor='#E57A63',edgecolor='#ba6223'))
            #         ax.text(Top_Average + Top_Average*0.5, (pos - delta / 2.0) - 0.18, str(np.round(Top_Average, 1)), fontsize=7)
            #         david_lx.append(Top_Average)
            #         david_ly.append(pos - delta / 2.0)
            #
            # else:
            ly.append(pos - delta / 2.0)
            lx.append(Low_Average)
            ax.add_patch(patches.Rectangle((Low_min, (pos - delta / 2.0) - 0.18), Low_max - Low_min, delta,
                                           facecolor='#d7d9db', edgecolor='#6d7378'))
            ax.text(Low_max + Low_Average / 6, (pos - delta / 2.0) - 0.18, str(np.round(Low_Average, 2)),
                    fontsize=7)
            writePointToList(pos, delta, Low_Average, ValueType)

            if High_Average > 0.0:
                ax.add_patch(patches.Rectangle((High_min, (pos - delta / 2.0) - 0.18), High_max - High_min, delta,
                                               facecolor='#d7d9db', edgecolor='#6d7378'))
                ax.text(High_Average + High_Average * 0.5, (pos - delta / 2.0) - 0.18,
                        str(np.round(High_Average, 1)), fontsize=7)

                writePointToList(pos, delta, High_Average, ValueType)

            if Top_Average > 0.0:
                ax.add_patch(patches.Rectangle((Top_min, (pos - delta / 2.0) - 0.18), Top_max - Top_min, delta,
                                               facecolor='#d7d9db', edgecolor='#6d7378'))
                ax.text(Top_Average + Top_Average * 0.5, (pos - delta / 2.0) - 0.18, str(np.round(Top_Average, 1)),
                        fontsize=7)
                writePointToList(pos, delta, Top_Average, ValueType)




    # calcalate average and plot average
    median = np.median(lx)
    stadard_median = 15.19
    average = np.average(lx)
    stdev = np.std(lx)

    # plot median for all of the data
    plt.axvline(x=median, color = '#ff9999', ls='dotted')
    # ax.text(median + 3, len(data)-2, ("Literature Search Median: " + str(int(np.round(median, 0))) + " um"),
    #         #+ " +/- " + str(np.round(stdev,0)),
    #         fontsize=11, color = '#ff4d4d')

    # plot media for the standard test dust
    # plt.axvline(x=stadard_median, color='#00e6ac', ls='dotted')
    # ax.text(stadard_median + 3, len(data) - 4, ("Standard Dust Median: " + str(int(np.round(stadard_median, 0))) + " um"),
    #         # + " +/- " + str(np.round(stdev,0)),
    #         fontsize=11, color='#00e6ac')

    ax.plot((low_min,low_max),(0,0))

    # plot all the data points "Mean from Reported Range"
    ax.plot(m_lx, m_ly, marker='v', color = '#737373', linewidth = 0, markersize=4)

    # plot all the data points "Reported Average"
    ax.plot(a_lx, a_ly, marker='s', color='#737373', linewidth=0, markersize=4)

    # plot all the data points "Mean from Reported Distribution"
    ax.plot(d_lx, d_ly, marker='o', color='#737373', linewidth=0, markersize=4)

    # plot Davids data points
    ax.plot(david_lx, david_ly, marker='s', color='#fc6c05', linewidth=0, markersize=4)

    # now get the limits as automatically computed
    xmin, xmax = ax.get_xlim()
    # and use them to draw the hlines in your example
    ax.grid(False)

    # Compose a legend
    stadanrdDust_patch = mpatches.Patch(facecolor='#00e6ac',
                                  edgecolor='#00b386', label='Size Range: Standard Test Dust')
    literatureDust_patch = mpatches.Patch(facecolor='#d7d9db', edgecolor='#6d7378', label='Size Range: Literature Search')
    providedDataPoints = mpatches.Patch(facecolor='#E57A63', edgecolor='#ba6223', label='Size Range: Data provided by Leo')
    #davidDust_patch = mpatches.Patch(facecolor='#fc954b', edgecolor='#ba6223', label='Size Range: Articles Provided by David Miller')
    meanPoint = mlines.Line2D([], [], marker='v', color='#737373',
                              markersize=5, label='Mean Calculated from Literature Reported Range')
    averagePoint = mlines.Line2D([], [], marker='s', color='#737373',
                                 markersize=5, label='Literature Reported Average')
    medianPoint = mlines.Line2D([], [], marker='o', color='#737373',
                                markersize=5, label='Mean from Literature Reported Distribution')

    # # Plot the legend
    plt.legend(
        handles=[literatureDust_patch,
                 #davidDust_patch,
                 stadanrdDust_patch, providedDataPoints, averagePoint, meanPoint, medianPoint], bbox_to_anchor=(1.05, 0.95), loc=2, borderaxespad=0.)

    # eventually return what we have done
    return ax


# this is the main script, note that we have imported pyplot as plt
rangedata = {}
f = open('csvData_withDavidTags.csv', 'rb')
reader = csv.reader(f)
for row in reader:
    i = row
    Name = str(i[0])
    Low_min = float(i[2])
    Low_max = float(i[4])
    Low_Average = float(i[3])
    Max_min = 0
    Max_max = 0
    Max_Average = 0
    Top_min = 0
    Top_max = 0
    Top_Average = 0
    Max = float(i[1])
    Method = str(i[11])
    David = str(i[12])
    ValueType = str(i[13])
    try:
        Max_min = float(i[5])
    except:
        donothing = None
    try:
        Max_max = float(i[7])
    except:
        donothing = None
    try:
        Max_Average = float(i[6])
    except:
        donothing = None
    try:
        Top_min = float(i[8])
    except:
        donothing = None
    try:
        Top_max = float(i[10])
    except:
        donothing = None
    try:
        Top_Average = float(i[9])
    except:
        donothing = None

    rangedata[Name] = (Max, Low_min, Low_max, Low_Average, Max_min, Max_max, Max_Average, Top_min, Top_max, Top_Average, Method, David, ValueType)
f.close()
# print rangedata

# standard dust types:
rangedata["PT-A1 Ultrafine"]=(22, 0.92,22,4.51,0,0,0,0,0,0,"","",'Mean from Reported Distribution')
rangedata["PT-A2 Fine"]=(176, 0.97,176.00,8.8,0,0,0,0,0,0,"","",'Mean from Reported Distribution')
rangedata["PT-A3 Medium"]=(176, 0.97,176,15.19306931,0,0,0,0,0,0,"","",'Mean from Reported Distribution')
rangedata["PT-A4 Course"]=(352, 0.97,352,36,0,0,0,0,0,0,"","",'Mean from Reported Distribution')
rangedata["ASTM C778 graded"]=(1180, 150,1180,369.444,0,0,0,0,0,0,"","",'Mean from Reported Distribution')


# call the function and give its result a name
ax = plot_rect(rangedata)
# so that we can further manipulate it using the `axes` methods, e.g.
ax.set_xlabel('Log of Particle Diameter [um]')
# finally save or show what we have
plt.show()
plt.savefig('Log of Particle Diameter', dpi=300)