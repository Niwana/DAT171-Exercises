import numpy as np
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
        #print(line)
        for item in line:
            npArray.append(float(item))
    npArray = np.array(npArray)
    #np.set_printoptions(threshold=np.nan)      # Prints out all items in a numpy list
    print(npArray)
    print(type(npArray))

    file1.close()


read_coordinate_file('SampleCoordinates.txt')

#end=time.time()

#print(end-time)