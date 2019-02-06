import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc
import time as t
from scipy.sparse import csr_matrix as csr

R = 1
start = t.time()


def mercator_projection(longitud, latitude):
    x = (R * (np.pi * float(longitud)) / 180)
    y = (R * np.log(np.tan((np.pi / 4) + ((np.pi * float(latitude)) / 360))))
    return x, y


# Read in coordinates from file and convert it into a list
def read_coordinate_file(filename):
    coords = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('{\n}')
            latitude, longitud = line.split(',')
            coord = mercator_projection(float(longitud), float(latitude))
            coords.append(coord)
    coord_list = np.array(coords)
    return coord_list


# end = t.time()
# print("Tidsåtgång: ", end - start)


def plot_points(coords, indices):
    line_segments = lc(coords[indices], color='gray', linewidths=0.2)
    ax = plt.gca()
    ax.add_collection(line_segments)
    plt.scatter(coords[:, 0], coords[:, 1], color='r', s=10)
    plt.show()


def construct_graph_connections(coord_list, radius):
    indices = []
    distances = []
    # distance_fn = dist.pdist(coord_list)

    for i, city_i in enumerate(coord_list):
        for j in range(i + 1, len(coord_list)):
            city_j = coord_list[j]
            distance = np.linalg.norm(city_i - city_j)
            if distance < radius:
                distances.append(distance)
                indices.append((i, j))
    costs = np.array(distances) ** (9 / 10)
    return np.array(indices), costs


def construct_graph(indices, costs, N):
    sparseGraph = (csr((costs, (indices[:, 0], indices[:, 1])), shape=(N, N)))
    return sparseGraph


coord_list = read_coordinate_file('HungaryCities.txt')
indices, costs = construct_graph_connections(coord_list, 0.005)
sparseGraph = construct_graph(indices, costs, len(coord_list))
plot_points(coord_list, indices)
