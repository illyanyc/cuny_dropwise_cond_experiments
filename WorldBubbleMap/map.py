# import the library
import folium
import pandas as pd
import math
from colour import Color
import json
from json import JSONEncoder
from folium import plugins
from scipy.ndimage import imread
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.image as mpimg
import numpy as np
import cv2



# Json encoder
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

# Color gradient methods:
#region
def parseValueDevide(list,fl):
    return_list = []
    for i in list:
        value = i / fl
        return_list.append(value)
        return return_list

def ParseValueLog(list,base,multiplier):
    return_list = []
    for i in list:
        value = math.log10(i)
        return_list.append(float(value+1))
    return return_list

def combineListValues(names, values, method):
    return_list = []
    counter = 0
    for i in names:
        newname = str(i)+str("<br>")+str("Diameter: ")+str(values[counter])+str(" um") \
                  +str("<br>")+str("Method: ")+str(method[counter])
        print newname
        return_list.append(newname)
        counter += 1

    return return_list

def generateColorGradient(color1, color2, n):
    color1 = Color(color1)
    colors = list(color1.range_to(Color(color2), n))
    return colors

def hex_to_RGB(hex):
  ''' "#FFFFFF" -> [255,255,255] '''
  # Pass 16 to the integer function for change of base
  return [int(hex[i:i+2], 16) for i in range(1,6,2)]

def RGB_to_hex(RGB):
  ''' [255,255,255] -> "#FFFFFF" '''
  # Components need to be integers for hex to make sense
  RGB = [int(x) for x in RGB]
  return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def color_dict(gradient):
  ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
  return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
      "r":[RGB[0] for RGB in gradient],
      "g":[RGB[1] for RGB in gradient],
      "b":[RGB[2] for RGB in gradient]}
#endregion
# Produce gradient from two colors and n number of values in list (to assign each color to a value later)
def gradient(start_hex, finish_hex, n):
  ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
  # Starting and ending colors in RGB form
  s = hex_to_RGB(start_hex)
  f = hex_to_RGB(finish_hex)
  # Initilize a list of the output colors with the starting color
  RGB_list = [s]
  # Calcuate a color at each evenly spaced value of t from 1 to n
  for t in range(1, n):
    # Interpolate RGB vector for color at the current value of t
    curr_vector = [
      int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
      for j in range(3)
    ]
    # Add it to our list of output colors
    RGB_list.append(curr_vector)

  return color_dict(RGB_list)

# Break down data by decate, make color gradients and sub-legends for each decate; call the method to make one comprehensive legend
def prepGradientByDecate(data, listofColors):

    valuesSortedByDecate = {}

    for i in data:

        if float(i) <= 1.0:
            valuesSortedByDecate.setdefault("lessThan1",[]).append(i)

        if float(i) > 1.0 and float(i) <= 10.0:
            valuesSortedByDecate.setdefault("lessThan10",[]).append(i)

        if float(i) > 10.0 and float(i) <= 100.0:
            valuesSortedByDecate.setdefault("lessThan100",[]).append(i)

        if float(i) > 100.0 and float(i) <= 1000.0:
            valuesSortedByDecate.setdefault("lessThan1000",[]).append(i)

        if float(i) > 1000.0:
            valuesSortedByDecate.setdefault("over1000",[]).append(i)

    # declate the lists of data sorted by decate
    lessThan1 = []
    lessThan10 = []
    lessThan100 = []
    lessThan1000 = []
    over1000 = []

    PNGList = []

    # Attempt to get the RGB range for all values and plot legends
    try:
        i = valuesSortedByDecate["lessThan1"]
        lessThan1 = (gradient(listofColors[0], listofColors[1], len(i)))['hex']
        l = plot_color_gradients(lessThan1, None, min(i), 1)
        PNGList.append(l)
    except: n = None
    try:
        i = valuesSortedByDecate["lessThan10"]
        lessThan10 = (gradient(listofColors[1], listofColors[2], len(i)))['hex']
        l = plot_color_gradients(lessThan10,  None, min(i), 2)
        PNGList.append(l)
    except: n = None
    try:
        i = valuesSortedByDecate["lessThan100"]
        lessThan100 = (gradient(listofColors[2], listofColors[3], len(i)))['hex']
        l = plot_color_gradients(lessThan100, None, min(i), 3)
        PNGList.append(l)
    except: n = None
    try:
        i = valuesSortedByDecate["lessThan1000"]
        lessThan1000 = (gradient(listofColors[3], listofColors[4], len(i)))['hex']
        l = plot_color_gradients(lessThan1000, max(i), min(i), 4)
        PNGList.append(l)

    except: n = None
    try:
        i = valuesSortedByDecate["over1000"]
        over1000 = (gradient(listofColors[4], listofColors[5], len(i)))['hex']
        l = plot_color_gradients(over1000, max(i), min(i), 5)
        PNGList.append(l)

    except: n = None


    # combine all of the lists into one long list
    colorlist = lessThan1 + lessThan10 + lessThan100 + lessThan1000 + over1000

    #create a comprehensive legend of all sub-legends
    mergeSubLegends(PNGList)

    return colorlist

# make a legend of a color gradient
def plot_color_gradients(_gradient, max, min, plotnumber):
    fig = plt.figure(figsize=(5, 1))
    ax = fig.add_subplot(111)
    x = 0
    y = 0
    h = 50
    w = 50

    if len(_gradient) < 20:
        new_gradient = gradient(_gradient[0], _gradient[len(_gradient)-1], 20 )["hex"]

        for i in new_gradient:
            rect = matplotlib.patches.Rectangle((x, y), h, w, facecolor=i, edgecolor=None)
            ax.add_patch(rect)
            x = x + w
    else:
        for i in _gradient:
            rect = matplotlib.patches.Rectangle((x, y), h, w, facecolor=i, edgecolor=None)
            ax.add_patch(rect)
            x = x + w

    if min is not None:
        ax.text(7, 5, str("{0:.1f}".format(min)),
                verticalalignment='bottom', horizontalalignment='left',
                color='black', fontsize=18)

    if max is not None:
        ax.text(x-7, 5, str("{0:.1f}".format(max)),
                verticalalignment='bottom', horizontalalignment='right',
                color='black', fontsize=18)

    plt.xlim(0, x)
    plt.ylim(0, 20)

    #plt.yaxis('off')
    ax.axes.get_yaxis().set_visible(False)
    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom='off',  # ticks along the bottom edge are off
        top='off',  # ticks along the top edge are off
        labelbottom='off')
    plt.gcf().subplots_adjust(bottom=0.5)
    name = "sub_Legend-"+str(plotnumber)+".png"
    plt.savefig(name,transparent=True )
    return name

# Combine all of the sub-Legends into one legend
def mergeSubLegends(l):
    fig = plt.figure("Legend")



    img_A = plt.imread(l[0])
    img_B = plt.imread(l[1])
    img_C = plt.imread(l[2])
    img_D = plt.imread(l[3])

    ax = fig.add_subplot(141)
    plt.imshow(img_A)
    plt.axis('off')

    ax.text(60, -25, "Legend: Particle Size (Diameter) [um]",
            verticalalignment='top', horizontalalignment='left',
            color='black', fontsize=9)

    ax = fig.add_subplot(142)
    plt.imshow(img_B)
    plt.axis('off')

    ax = fig.add_subplot(143)
    plt.imshow(img_C)
    plt.axis('off')

    ax = fig.add_subplot(144)
    plt.imshow(img_D)
    plt.axis('off')



    plt.subplots_adjust(left=0.01, bottom=None, right=0.99, top=1.75, wspace=-0.225, hspace=0)
    plt.savefig('legend.png', dpi=150, transparent=True)


# Import data from CSV
csvdata = pd.read_csv("data.csv", header=0)
name = list(csvdata.Name)
lon = list(csvdata.Latitude)
lat = list(csvdata.Longitude)
value= list(csvdata.mid)
method= list(csvdata.Method)
value_log = ParseValueLog(value,10,1)
name_to_plot = combineListValues(name, value, method)


# Make a data frame with dots to show on the map
data = pd.DataFrame({
    'lat': lat,
    'lon': lon,
    'name': name_to_plot,
    'value': value_log,
    'valueraw': value
})
data

# sort data by value
data = data.sort_values(by=('value'), ascending=True)

# Gerenrate colour gradient with n = number of items in the list
# Old gradient formula
#colorgradient = gradient("#3498DB", "#E74C3C", len(name))

# Create lsit of colors to be used for subgradients
listOfColors_toPass = ['#0000db',
                '#00dbd7',
                '#00db03',
                '#dbd700',
                '#db1900',
                '#db00d0']

# get the color gradient to color the plotted data points
colorgradient = prepGradientByDecate(data["valueraw"], listOfColors_toPass)

# Make an empty map
m = folium.Map(location=[20, 0], tiles='cartodbpositron', zoom_start=2)

# Enclose all of the Un-localized data into a circle
#region
folium.Circle(
        location=[-39, -13],
        popup=("No specific location reported in literature:"),
        #radius=data.iloc[i]['value'] * 100000,
        radius= (2)*
                ((-(0.0000992*(abs(-39))))-(0.0021852*(abs(-13)))+1)
                 * 850000,
        color="#000000",
        fill=True,
        fill_color="#ffffff"
    ).add_to(m)
#endregion
# add data points to map one by one
counter = 0
for i in range(0, len(data)):
    colors = colorgradient
    folium.Circle(
        location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
        popup=(data.iloc[i]['name']),
        #radius=data.iloc[i]['value'] * 100000,
        radius= (2)*
                ((-(0.0000992*(abs(data.iloc[i]['lon']**2))))-(0.0021852*(abs(data.iloc[i]['lon'])))+1)
                 * 50000,
        color=colorgradient[counter],
        fill=True,
        fill_color=colorgradient[counter]
    ).add_to(m)
    counter += 1

min_lon = 120
max_lon = 170
min_lat = 50
max_lat = 56

# Overlay the image
#m.add_child(plugins.ImageOverlay(data, opacity=0.8, bounds =[[min_lat, min_lon], [max_lat, max_lon]]))

# Save it as html
m.save('mymap.html')

#<div><img src="http://www.condensationexperiments.com/WorldBubbleMap/legend.png" alt="Legend"></div>
#<div><img src="http://www.condensationexperiments.com/WorldBubbleMap/Figure_1.png" alt="Chart"></div>
# Change height to 90%






# Try another type of plot BETA
m = folium.Map(location=[20, 0], tiles='cartodbpositron', zoom_start=2)
counter = 0
for i in range(0, len(data)):
    colors = colorgradient
    folium.Circle(
        location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
        popup=(data.iloc[i]['name']),
        #radius=data.iloc[i]['value'] * 100000,
        radius= (data.iloc[i]['value'])*
                ((-(0.0000992*(abs(data.iloc[i]['lon']**2))))-(0.0021852*(abs(data.iloc[i]['lon'])))+1)
                 * 1000,
        color= "#1F618D",
        fill=True,
        fill_color=colors[counter]
    ).add_to(m)
    counter += 1
# Overlay the image
#m.add_child(plugins.ImageOverlay(data, opacity=0.8, bounds =[[min_lat, min_lon], [max_lat, max_lon]]))
# Save it as html
m.save('mymap2.html')