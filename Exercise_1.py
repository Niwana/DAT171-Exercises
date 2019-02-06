import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc
import time as t
from scipy.spatial import distance as dist

R = 1
start = t.time()


# Read in coordinates from file and convert it into a list
def read_coordinate_file(filename):
    file = open(filename, 'r')
    npArray = []
    cities = []
    for line in file:
        line = line.strip('{\n}')
        line = line.replace(' ', '')
        line = line.split(',')
        for item in line:
            npArray.append(float(item))
    npArray = np.array(npArray)
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

end = t.time()
#print("Tidsåtgång: ", end - start)

coord_list = read_coordinate_file('SampleCoordinates.txt')

def plot_points(xy):
    for cities in xy:
        plt.scatter(cities[0], cities[1], color='r', s=10)
    plt.show()


def construct_graph_connections(coord_list, radius):
    index = []
    cities_tillf = []
    distance = []
    distance_fn = dist.pdist(coord_list)

    for i , city in enumerate(coord_list):
        for j , city in enumerate(coord_list):
            if j <= i:
                pass
            else:
                index.append(i)
                index.append(j)

    for k in range (len(distance_fn)):
        if distance_fn[k] <= radius:
            distance.append(distance_fn[k])
            cities_tillf.append(np.array(index).reshape(-1,2)[k])

    cities=np.array(cities_tillf)
    cost_tillf = np.array(distance) ** (9 / 10)
    #print(cost)
    cost=cost_tillf.reshape(-1,1)

    return cities.reshape(-1,2) , cost

cities, cost = construct_graph_connections(coord_list, 0.08)

print(cities)
print(cost)


'''
def construct_graph_connections(coord_list, radius):
    index = []
    cities = []
    distance = []
    costArray = np.array([])
    indicies = np.array([]
    distance_fn = dist.pdist(coord_list)

    ''''''
    for city1, i in enumerate(coord_list):
        for
    city2, j in enumerate(coord_list):
    #    if (i != j).all():
    distance = np.sqrt((j[0] - i[0]) ** 2 + (j[1] - i[1]) ** 2)  # x2-x1, y2-y1
    print("x1:", i[0], "y1:", i[1], "x2:", j[0], "y2:", j[1], )
    print("distance:", distance)
    if distance <= radius:
        cost = distance ** (9 / 10)
    costArray = np.append(costArray, cost)
    print("City:", city1, "and city:", city2)
    print("TRUE\n")
    indicies = np.append(indicies, city1)
    indicies = np.append(indicies, city2)
    else:
    print("City:", city1, "and city:", city2)
    print("FALSE\n")
    indicies = indicies.reshape(-1, 2)
    costArray = costArray.reshape(-1, 1)
    print("City x       City y      Cost\n", np.concatenate((indicies, costArray), axis=1))  # Only for visual
    # print(indicies, costArray)

    #plot_points(coord_list)
#
'''


'''
def plot_points2(coord_list):
    lines = []
    for cities in coord_list:
        #plt.scatter(cities[0], cities[1], color='r')
        #print(cities)
        lines.append((cities[0], cities[1]))
    line_segments = lc([lines],linestyles='dotted')
    fig = plt.figure()
    ax = fig.gca()
    ax.add_collection(line_segments)
    ax.set_ylim((-0.1,0.2))
    ax.set_xlim((-0.1, 0.1))
    print(line_segments)
    plt.show()
plot_points2(coord_list)
'''