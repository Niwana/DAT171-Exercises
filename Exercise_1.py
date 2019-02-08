import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc
import time as t
from scipy.sparse import csr_matrix as csr
from scipy.sparse import csgraph
from scipy.spatial import cKDTree as ckd


R = 1


# Se över om våra funktioners argument ska ha samma namn som de globala variablerna
def mercator_projection(longitud, latitude):
    x = (R * (np.pi * float(longitud)) / 180)
    y = (R * np.log(np.tan((np.pi / 4) + ((np.pi * float(latitude)) / 360))))
    return x, y


# Read in coordinates from file and store them in an array
def read_coordinate_file(filename):
    coords = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('{\n}')
            latitude, longitud = line.split(',')
            coord = mercator_projection(float(longitud), float(latitude))
            coords.append(coord)
    coord_list = np.array(coords)   # Kan man skippa detta steg och returna coords som en np array?
    return coord_list


def plot_points(coords, indices, chosenPath):   # !!! cord_list är detsamma som coords. Vilket namn ska vi köra på?!!!
    radius_segments = lc(coords[indices], color='gray', linewidths=0.2)
    path_segment = lc(coords[np.array(chosenPath)], color='blue', linewidths=2)
    plt.scatter(coords[:, 0], coords[:, 1], color='r', s=10)

    ax = plt.gca()
    ax.add_collection(radius_segments)
    ax.add_collection(path_segment)
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


# Creates a sparse graph which is later used for dijkstra
def construct_graph(indices, costs, N):
    sparseGraph = (csr((costs, (indices[:, 0], indices[:, 1])), shape=(N, N)))
    return sparseGraph


def cheapest_path(sparseGraph, start_node, end_node):
    cost_matrix, predecessor_matrix = csgraph.dijkstra(sparseGraph, directed=False, indices=start_node, return_predecessors=True)
    return cost_matrix[end_node], predecessor_matrix


def compute_path(predecessor_matrix, start_node, end_node):
    path = []
    while end_node != start_node:
        path.append(end_node)
        end_node = predecessor_matrix[end_node]
    path.append(end_node)
    path.reverse()
    return path


def path_to_array(path):
    pathIndices = []
    for i in range(len(path)-1):
        pathIndices.append([path[i], path[i+1]])
        #print(pathIndices)
    return pathIndices


def construct_fast_graph_connections(coords, radius):
    p = coords
    tree = ckd(p)
    distance, index = tree.query((0, 0.07), k=3)
    print("idx\n", index)
    print("p[idx]\n", p[index])
    print("distance\n", distance)
    return indices, costs

'''
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
'''

start_node = 0
end_node = 5
search_radius = 0.08


start_time = t.time()
time = t.time()
coord_list = read_coordinate_file('SampleCoordinates.txt')
print('| Time read coordinate file: {:4.4f}s'.format(t.time() - time))

time = t.time()
indices, costs = construct_graph_connections(coord_list, search_radius)
indices2, costs2 = construct_fast_graph_connections(coord_list, search_radius)
print('| Time construct graph connections: {:4.4f}s'.format(t.time() - time))

#print("indicies", indices)
#print("costs", costs)
#print("indicies2", indices2)
#print("costs2", costs2)

time = t.time()
sparseGraph = construct_graph(indices, costs, len(coord_list))
cost, predecessor_matrix = cheapest_path(sparseGraph, start_node, end_node)
chosenPath = compute_path(predecessor_matrix, start_node, end_node)
chosenPathIndices = path_to_array(chosenPath)
print('| Time calculate shortest path: {:4.4f}s'.format(t.time() - time))

print('| The whole program took: {:4.4f}s'.format(t.time() - start_time))
print(f'\nThe cheapest path between city {start_node} and city {end_node} costs: {cost}')




plot_points(coord_list, indices, chosenPathIndices)