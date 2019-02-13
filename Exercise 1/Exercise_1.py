import time as t
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lC
from scipy.sparse import csgraph, csr_matrix as csr
from scipy.spatial import cKDTree as cKD


R = 1


def mercator_projection(latitude: [float], longitude: [float]) -> [float]:
    """
    Mercator projection of a given geographical point (latitude, longitude).


    Parameters:
    :param longitude: Geographical coordinate of a north-south position
    :param latitude: Geographical coordinate of an east-west position

    Returns:
    :return x: Cylindrical x projection
    :return y: Cylindrical y projection
    """
    x = (R * (np.pi * float(longitude)) / 180)
    y = (R * np.log(np.tan((np.pi / 4) + ((np.pi * float(latitude)) / 360))))
    return x, y


# ------------------------------------------------------
# Read coordinates from file and store them in an array.
def read_coordinate_file(filename):
    coords = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('{\n}')
            latitude, longitude = line.split(',')

            # Convert from lat-long to x-y using the mercator projection
            coord = mercator_projection(float(latitude), float(longitude))
            coords.append(coord)
    return np.array(coords)


# -------------------------------------------------------------------------
# Plot all points, connections and the cheapest path from the start node to
# the end node.
def plot_points(coords, indices, path):
    time_plot = t.time()

    # creates a line collection of the nodes within a given radius and a
    # separate line collection of the cheapest path
    radius_segments = lC(coords[indices], color='gray', linewidths=0.2)
    path_segment = lC(coords[np.array(path)], color='blue', linewidths=2)
    plt.scatter(coords[:, 0], coords[:, 1], color='r', s=10)

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.add_collection(radius_segments)
    ax.add_collection(path_segment)
    print('| Time spent plotting: {:4.4f}s'.format(t.time() - time_plot))
    plt.show()


# ---------------------------------------------------------------------------
# Determines neighbouring nodes for each node, and calculates the travel cost
# if within a given radius.
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


# ---------------------------------------------------------------------------
# Determines neighbouring nodes for each node, and calculates the travel cost
# if within a given radius.
def construct_fast_graph_connections(coords, radius):
    tree = cKD(coords)
    indices = []
    distances = []
    for i in range(len(coords)):
        filtered_city = tree.query_ball_point(coords[i], r=radius)
        new_neighbours = [k for k in filtered_city if k > i]
        for j in range(0, len(new_neighbours)):
            indices.append((i, new_neighbours[j]))
            distances.append(np.linalg.norm(coords[i] - coords[new_neighbours[j]]))
    costs = np.array(distances) ** (9 / 10)
    return np.array(indices), costs


# -------------------------------------------------------------------------------
# Creates a compressed sparse row matrix of the travel costs associated with each
# node connection.
def construct_graph(indices, costs, N):
    s_graph = (csr((costs, (indices[:, 0], indices[:, 1])), shape=(N, N)))
    return s_graph


# --------------------------------------------------------------------------------
# Finds the cheapest path through a sparse graph utilizing the Dijkstra algorithm.
def cheapest_path(s_graph, start, end):
    cost_matrix, predecessors = csgraph.dijkstra(s_graph, directed=False, indices=start,
                                                 return_predecessors=True)
    return cost_matrix[end], predecessors


# ------------------------------------------------------------
# Converts a node predecessor matrix into a sequence of nodes.
def compute_path(predecessors, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = predecessors[current]
    path.append(current)
    path.reverse()
    return path


# ------------------------------------------------------------------------------
# Takes the indices from chosen path and groups them into pairs of node indices,
# which lineCollection can use to print the cheapest path.
def path_to_array(path):
    path_indices = []
    for i in range(len(path) - 1):
        path_indices.append([path[i], path[i + 1]])
    return path_indices


# ------------------------
# User input and main code
start_time = t.time()
start_node = 1573
end_node = 10584
search_radius = 0.0025
coord_list = read_coordinate_file('GermanyCities.txt')
time_read_coord = t.time()


# ------------------------------------------------------------------
# Determine intercity-connections using a manual method or a kd-tree
start2_time = t.time()
# city_indices, travel_costs = construct_graph_connections(coord_list, search_radius)
city_indices, travel_costs = construct_fast_graph_connections(coord_list, search_radius)
time_construct_graph_connections = t.time()


# -------------------------------------------------------------------
# Find and draw the cheapest path between the start node and end node
start3_time = t.time()
sparse_graph = construct_graph(city_indices, travel_costs, len(coord_list))
path_cost, predecessor_matrix = cheapest_path(sparse_graph, start_node, end_node)
chosen_path = compute_path(predecessor_matrix, start_node, end_node)
chosen_path_indices = path_to_array(chosen_path)
time_calc_shortest_path = t.time()

print(f'\nThe cheapest path between city {start_node} and city {end_node} costs: {path_cost}\n'
      f'and consists of cities {chosen_path}\n')
print('| Time read coordinate file: {:4.4f}s'.format(time_read_coord - start_time))
print('| Time construct *graph connections: {:4.4f}s'.format(time_construct_graph_connections - start2_time))
print('| Time calculate shortest path: {:4.4f}s'.format(time_calc_shortest_path - start3_time))
print('| Time running the entire program: {:4.4f}s'.format(time_calc_shortest_path - start_time))

plot_points(coord_list, city_indices, chosen_path_indices)