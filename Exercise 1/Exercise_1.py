import time as t
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lC
from scipy.sparse import csgraph, csr_matrix as csr
from scipy.spatial import cKDTree as cKD
import math

R = 1
start_time = t.time()
start_node = 1573
end_node = 10584
search_radius = 0.0025
country = 'GermanyCities.txt'

time_read_coord = t.time()

# TODO: kommentera utförligare

def mercator_projection(latitude: float, longitude: float) -> tuple((float, float)):
    """
    Mercator projection of a given geographical point (latitude, longitude).


    Parameters:
    :param longitude: Geographical coordinate of a north-south position
    :param latitude: Geographical coordinate of an east-west position

    Returns:
    :return x: Cylindrical x projection
    :return y: Cylindrical y projection
    """
    x = (R * (np.pi * longitude) / 180)
    y = (R * np.log(np.tan((np.pi / 4) + ((np.pi * latitude) / 360))))
    return x, y


def read_coordinate_file(filename):
    """ Read coordinates from file and store them in an array.

    :param filename:
    :return:
    """
    coords = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('{\n}')
            latitude, longitude = line.split(',')

            # Convert from lat-long to x-y using the mercator projection
            coord = mercator_projection(float(latitude), float(longitude))
            coords.append(coord)
    return np.array(coords)


def plot_points(coords, indices, path):
    """ Plot all points, connections and the cheapest path from the start node to
        the end node.

    :param coords:
    :param indices:
    :param path:
    :return:
    """
    time_plot = t.time()
    path_to_tuples = []
    for cities in coords[path]:
        path_to_tuples.append(tuple(cities))

    # creates a line collection of the nodes within a given radius and a
    # separate line collection of the cheapest path
    radius_segments = lC(coords[indices], color='gray', linewidths=0.2)
    path_segment = lC([path_to_tuples], color='blue', linewidths=2)
    plt.scatter(coords[:, 0], coords[:, 1], color='r', s=10)

    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.add_collection(radius_segments)
    ax.add_collection(path_segment)
    print('| Time spent plotting: {:4.4f}s'.format(t.time() - time_plot))
    plt.show()


def construct_graph_connections(coords, radius):
    """ Determines neighbouring nodes for each node, and calculates the travel cost
        if within a given radius.

    :param coords:
    :param radius:
    :return:
    """
    indices = []
    distances = []
    for i, current_city in enumerate(coords):
        for j, other_city in enumerate(coords[i+1:]):
            distance = math.sqrt(((current_city[0] - other_city[0]) ** 2) + (current_city[1] - other_city[1]) ** 2)
            if distance < radius:
                distances.append(distance)
                indices.append((i, j))
    costs = np.array(distances) ** (9 / 10)
    return np.array(indices), costs


def construct_fast_graph_connections(coords, radius):
    """ Determines neighbouring nodes for each node, and calculates the travel cost
        if within a given radius.

    :param coords:
    :param radius:
    :return:
    """
    tree = cKD(coords)
    indices = []
    distances = []
    for i in range(len(coords)):
        filtered_city = tree.query_ball_point(coords[i], r=radius)
        new_neighbours = [k for k in filtered_city if k > i]
        for j in range(0, len(new_neighbours)):
            indices.append((i, new_neighbours[j]))
            distances.append(math.sqrt(((coords[i][0] - coords[new_neighbours[j]][0]) ** 2) +
                                        (coords[i][1] - coords[new_neighbours[j]][1]) ** 2))
    costs = np.array(distances) ** (9 / 10)
    return np.array(indices), costs


def construct_graph(indices, costs, N):
    """ Creates a compressed sparse row matrix of the travel costs associated with each
    node connection. The SciPy sparse row matrix function takes the following input arguments:

    :param indices: indices of the connected nodes. Each index is split into start nodes and end
    nodes for each connection. This is equivalent to the transposed indices matrix.
    :param costs: the costs associated with each node connection
    :param N: is the size of the sparse graph
    :return: a SciPy compressed sparse row matrix describing the costs associated with each node connection.
    """
    s_graph = csr((costs, (indices[:, 0], indices[:, 1])), shape=(N, N))
    return s_graph


def cheapest_path(s_graph, start, end):
    """
    Dijkstra calculates the shortest path between nodes in a sparse graph.

    :param s_graph: includes the costs between the nodes which are in close distance to each other.
    :param start: start node
    :param end: end node
    :return: a cost matrix which consists of the shortest path from start node to end node.
            predecessors is a list of all the nodes which are
    """
    cost_matrix, predecessors = csgraph.dijkstra(s_graph, directed=False, indices=start, return_predecessors=True)
    return cost_matrix[end], predecessors


def compute_path(predecessors, start, end):
    # TODO: kommentera reverse, ordningen
    """ Converts a node predecessor matrix into a sequence of nodes.

    :param predecessors:
    :param start:
    :param end:
    :return:
    """
    path = []
    current = end
    while current != start:
        path.append(current)
        current = predecessors[current]
    path.append(current)
    path.reverse()
    return path



coord_list = read_coordinate_file(country)
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

time_calc_shortest_path = t.time()

print(f'\nThe cheapest path between city {start_node} and city {end_node} costs: {path_cost}\n'
      f'and consists of cities {chosen_path}\n')
print('| Time read coordinate file: {:4.4f}s'.format(time_read_coord - start_time))
print('| Time construct *graph connections: {:4.4f}s'.format(time_construct_graph_connections - start2_time))
print('| Time calculate shortest path: {:4.4f}s'.format(time_calc_shortest_path - start3_time))
print('| Time running the entire program: {:4.4f}s'.format(time_calc_shortest_path - start_time))

plot_points(coord_list, city_indices, chosen_path)

#print(coord_list[chosen_path])
new = []
for i in coord_list:
    new.append(tuple(i))
print([new])
a = [[(0.0349, 0.1400), (0.01745, 0.087377), (0.0349, 0.1400), (0.01745, 0.087377), (0.0349, 0.1400), (0.01745, 0.087377), (0.0349, 0.1400), (0.01745, 0.087377)]]
print('a', a)