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

def combineListValues(names, values):
    return_list = []
    counter = 0
    for i in names:
        newname = str(i)+str("<br>")+str(values[counter])+str(" microns")
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

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def plot_color_gradients(gradient, value):
    fig = plt.figure(figsize=(5, 1))
    ax = fig.add_subplot(111)
    x = 0
    y = 0
    h = 50
    w = 50

    value = sorted(value)
    ax.set_xlabel('Particle Size (microns)',color='black', fontsize=14)

    for i in reversed(gradient):
        rect = matplotlib.patches.Rectangle((x, y), h, w, color=i)
        ax.add_patch(rect)
        x = x + w

    ax.text(7, 5, str(value[0]),
            verticalalignment='bottom', horizontalalignment='left',
            color='black', fontsize=18)

    ax.text(x-7, 5, str(value[len(value)-1]),
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
    plt.savefig('legend.png')

# Import data from CSV
csvdata = pd.read_csv("data.csv", header=0)
name = list(csvdata.Name)
lon = list(csvdata.Latitude)
lat = list(csvdata.Longitude)
value= list(csvdata.low)
value_log = ParseValueLog(value,10,1)
name_to_plot = combineListValues(name, value)

# Make a data frame with dots to show on the map
data = pd.DataFrame({
    'lat': lat,
    'lon': lon,
    'name': name_to_plot,
    'value': value_log,
    'valueraw': value
})
data

data = data.sort_values(by=('value'), ascending=False)

# Gerenrate colour gradient with n = number of items in the list
colorgradient = gradient("#3498DB", "#E74C3C", len(name))


# Make an empty map
m = folium.Map(location=[20, 0], tiles='cartodbpositron', zoom_start=2)

# I can add marker one by one on the map
counter = 0
for i in range(0, len(data)):
    colors = colorgradient["hex"]
    folium.Circle(
        location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
        popup=(data.iloc[i]['name']),
        #radius=data.iloc[i]['value'] * 100000,
        radius= (2)*
                ((-(0.0000992*(abs(data.iloc[i]['lon']**2))))-(0.0021852*(abs(data.iloc[i]['lon'])))+1)
                 * 100000,
        color=colorgradient["hex"][counter],
        fill=True,
        fill_color=colorgradient["hex"][counter]
    ).add_to(m)
    counter += 1

# create Legend
plot_color_gradients(colorgradient["hex"], value)

min_lon = 120
max_lon = 170
min_lat = 50
max_lat = 56

# Overlay the image
#m.add_child(plugins.ImageOverlay(data, opacity=0.8, bounds =[[min_lat, min_lon], [max_lat, max_lon]]))


# Save it as html
m.save('mymap.html')

#<div><img src="http://www.condensationexperiments.com/WorldBubbleMap/legend.png" alt="Legend"></div>
# Change height to 90%





# Try another type of plot BETA

m = folium.Map(location=[20, 0], tiles='cartodbpositron', zoom_start=2)

counter = 0
for i in range(0, len(data)):
    colors = colorgradient["hex"]
    folium.Circle(
        location=[data.iloc[i]['lon'], data.iloc[i]['lat']],
        popup=(data.iloc[i]['name']),
        #radius=data.iloc[i]['value'] * 100000,
        radius= (data.iloc[i]['value'])*
                ((-(0.0000992*(abs(data.iloc[i]['lon']**2))))-(0.0021852*(abs(data.iloc[i]['lon'])))+1)
                 * 100000,
        color= "#1F618D",
        fill=True,
        fill_color=colors[counter]
    ).add_to(m)
    counter += 1

# create Legend
plot_color_gradients(colorgradient["hex"], value)

# Overlay the image
#m.add_child(plugins.ImageOverlay(data, opacity=0.8, bounds =[[min_lat, min_lon], [max_lat, max_lon]]))


# Save it as html
m.save('mymap2.html')