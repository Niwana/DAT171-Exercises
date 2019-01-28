#import time


#start=time.time()
def read_coordinate_file(filename):
    file1 = open(filename, 'r')
    for line in file1:
        line = line.strip("{}\n ").split(',')
        print(line)

    file1.close()
read_coordinate_file('SampleCoordinates.txt')

#end=time.time()

#print(end-time)