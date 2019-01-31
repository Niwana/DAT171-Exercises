import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc


import time as t



#start=time.time()

# Read in coordinates from file and convert it into a list
def read_coordinate_file(filename):
    file1 = open(filename, 'r')
    npArray = []
    for line in file1:
        line = line.strip('{\n}')
        line = line.replace(' ', '')
        line = line.split(',')
        for item in line:
            npArray.append(float(item))
    npArray = np.array(npArray)
    np.set_printoptions(threshold=np.nan)      # Prints out all items in a numpy list
    return npArray.reshape(-1, 2)
    file1.close()

coord_list = read_coordinate_file('HungaryCities.txt')
#print(coord_list)



def plot_points(coord_list):
    for cities in coord_list:
        plt.scatter(cities[0], cities[1], color='r')
        #print(cities[0])
    plt.show()


def plot_points2(coord_list):
    lines = []
    for cities in coord_list:
        #plt.scatter(cities[0], cities[1], color='r')
        #print(cities)
        lines.append( (cities[0], cities[1]) )
    #plt.show()

    line_segments = lc([lines],linestyles='dotted')
    fig = plt.figure()
    ax = fig.gca()
    ax.add_collection(line_segments)
    ax.set_ylim((15,23))
    ax.set_xlim((45, 49))
    print(line_segments)
    plt.show()


plot_points(coord_list)
plot_points2(coord_list)

#end=time.time()

#print(end-time)
