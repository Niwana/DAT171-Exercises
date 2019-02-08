
from scipy.spatial import cKDTree
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection as lc
import time as t
from scipy.sparse import csr_matrix as csr
from scipy.sparse import csgraph
from scipy.spatial import cKDTree as ckd

R = 1
START_NODE = 0
END_NODE = 5
SEARCH_RADIUS = 0.08

radius = 1
xy = [[0, 2], [0, 4], [1, 2], [1, 3], [1, 5], [2, 3], [2, 4], [3, 4], [3, 5], [3, 6], [4, 6], [5, 6]]

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
help(cKDTree)

coord_list = read_coordinate_file('SampleCoordinates.txt')
tree = cKDTree(coord_list)
#dd, ii = tree.query([1, 3], k=[4])
a = tree.query_ball_point([0,0], radius)
print("final", a)

print(coord_list)