import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc
import time as t
from scipy.sparse import csr_matrix as csr
from scipy.sparse import csgraph


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


def plot_points(coords, indices, chosenPath):
    line_segments = lc(coords[indices], color='gray', linewidths=0.2)

    segs = coords[chosenPath]
    #path_segment = lc(segs, color='r', linediwth=1)

    print(segs)
    ax = plt.gca()
    ax.add_collection(line_segments)
    #ax.add_collection(path_segment)
    plt.scatter(coords[:, 0], coords[:, 1], color='r', s=10)
    plt.show()


def construct_graph_connections(coord_list, radius):
    indices = []
    distances = []

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
    #print(sparseGraph)
    return sparseGraph


def cheapest_path(sparseGraph, start_node, end_node):
    cost_matrix, predecessor_matrix = csgraph.dijkstra(sparseGraph, directed=False, indices=start_node, return_predecessors=True)
    return cost_matrix[end_node], predecessor_matrix


def compute_path(predecessor_matrix, start_node, end_node):
    i = end_node
    path=[i]
    while i != start_node:
        path.append(predecessor_matrix[i])
        i = predecessor_matrix[i]
    return path[::-1]

coord_list = read_coordinate_file('SampleCoordinates.txt')
indices, costs = construct_graph_connections(coord_list, 0.08)
sparseGraph = construct_graph(indices, costs, len(coord_list))
cost, predecessor_matrix = cheapest_path(sparseGraph, start_node=0, end_node=5)
chosenPath = compute_path(predecessor_matrix, start_node=0, end_node=5)

#print(chosenPath)
#print(coord_list)
#print(coord_list[chosenPath])

plot_points(coord_list, indices, chosenPath)
#print(csgraph.reconstruct_path(sparseGraph, predecessor_matrix, directed=False))
help(lc)

