import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc
import time as t
from scipy.sparse import csr_matrix as csr
from scipy.sparse import csgraph
from scipy.spatial import cKDTree as ckd


R = 1

# Se över om våra funktioners argument ska ha samma namn som de globala variablerna
def mercator_projection(longitude, latitude):
    """
    :param longitude:
    :param latitude:
    :return:
    """
    x = (R * (np.pi * float(longitude)) / 180)
    y = (R * np.log(np.tan((np.pi / 4) + ((np.pi * float(latitude)) / 360))))
    return x, y


# Read in coordinates from file and store them in an array
def read_coordinate_file(filename):
    coords = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('{\n}')
            latitude, longitude = line.split(',')
            coord = mercator_projection(float(longitude), float(latitude))
            coords.append(coord)
    return np.array(coords)


def plot_points(coords, indices, path):
    radius_segments = lc(coords[indices], color='gray', linewidths=0.2)
    path_segment = lc(coords[np.array(path)], color='blue', linewidths=2)
    plt.scatter(coords[:, 0], coords[:, 1], color='r', s=10)

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.add_collection(radius_segments)
    ax.add_collection(path_segment)
    plt.show()


def construct_graph_connections(coords, radius):
    indices = []
    distances = []
    for i, city_i in enumerate(coords):
        for j in range(i + 1, len(coords)):
            city_j = coords[j]
            distance = np.linalg.norm(city_i - city_j)
            if distance < radius:
                distances.append(distance)
                indices.append((i, j))
    costs = np.array(distances) ** (9 / 10)
    return np.array(indices), costs


def construct_fast_graph_connections(coords, radius):
    tree = ckd(coords)
    indices = []
    distances = []
    for i in range(len(coords)):
        filtered_city = tree.query_ball_point(coords[i], r=radius, n_jobs=-1)
        new_neighbours = [k for k in filtered_city if k > i]
        for j in range(0, len(new_neighbours)):
            indices.append((i, new_neighbours[j]))
            distances.append(np.linalg.norm(coords[i] - coords[new_neighbours[j]]))
    costs = np.array(distances)**(9/10)
    return np.array(indices), costs


# Creates a sparse graph which is later used for dijkstra
def construct_graph(indices, costs, N):
    sparse_graph = (csr((costs, (indices[:, 0], indices[:, 1])), shape=(N, N)))
    return sparse_graph


def cheapest_path(sparse_graph, start_node, end_node):
    cost_matrix, predecessors = csgraph.dijkstra(sparse_graph, directed=False, indices=start_node, return_predecessors=True)
    return cost_matrix[end_node], predecessors


def compute_path(predecessors, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = predecessors[current]
    path.append(current)
    path.reverse()
    return path


# Takes the indices from chosen path and groups them into pairs of city indices,
# which lineCollection can use to print the cheapest path.
def path_to_array(path):
    path_indices = []
    for i in range(len(path) - 1):
        path_indices.append([path[i], path[i + 1]])
    return path_indices


start_node = 1573
end_node = 10584
search_radius = 0.0025

start_time = t.time()
time = t.time()
coord_list = read_coordinate_file('GermanyCities.txt')
print('| Time read coordinate file: {:4.4f}s'.format(t.time() - time))

time = t.time()

#city_indices, travel_costs = construct_graph_connections(coord_list, search_radius)
city_indices, travel_costs = construct_fast_graph_connections(coord_list, search_radius)

print('| Time fast_graph_connections: {:4.4f}s'.format(t.time() - time))
print('| Time construct graph connections: {:4.4f}s'.format(t.time() - time))

time = t.time()
sparse_graph = construct_graph(city_indices, travel_costs, len(coord_list))
path_cost, predecessor_matrix = cheapest_path(sparse_graph, start_node, end_node)
chosen_path = compute_path(predecessor_matrix, start_node, end_node)
chosen_path_indices = path_to_array(chosen_path)

print('| Time calculate shortest path: {:4.4f}s'.format(t.time() - time))
print('| The whole program took: {:4.4f}s'.format(t.time() - start_time))
print(f'\nThe cheapest path between city {start_node} and city {end_node} costs: {path_cost}\nand consists of cities {chosen_path}')

plot_points(coord_list, city_indices, chosen_path_indices)
