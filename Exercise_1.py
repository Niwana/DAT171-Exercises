import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc
import time as t

R = 1
start=t.time()

# Read in coordinates from file and convert it into a list
def read_coordinate_file(filename):
    file = open(filename, 'r')
    npArray = []
    for line in file:
        line = line.strip('{\n}')
        line = line.replace(' ', '')
        line = line.split(',')
        for item in line:
            npArray.append(float(item))

    npArray = np.array(npArray)
    #np.set_printoptions(threshold=np.nan)      # Prints out all items in a numpy list
    npArray2 = npArray.reshape(-1, 2)

    lat = npArray2[:, 0]
    long = npArray2[:, 1]

    x = (R * (np.pi * long) / 180)
    y = (R * np.log(np.tan((np.pi / 4) + ((np.pi * lat) / 360))))

    x = x.reshape(-1, 1)  # ful lösning, hitta bättre metod
    y = y.reshape(-1, 1)
    xy = np.hstack((x, y))

    return xy
    file.close()


end=t.time()
print("Tidsåtgång: ", end-start)

def plot_points(xy):
    for cities in xy:
        plt.scatter(cities[0], cities[1], color='r')
    plt.show()

coord_list = read_coordinate_file('HungaryCities.txt')
plot_points(coord_list)


'''
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



plot_points2(coord_list)
'''