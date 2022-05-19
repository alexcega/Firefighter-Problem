from os import listdir
from os.path import isfile, join
import numpy as np
import ffp
mypath ='Instances/GEN'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

a_map = [[]]
for one_file in onlyfiles:

# with open(mypath+"/"+'50_ep0.2_0_gilbert_9.in', "r") as map_file :
    with open(mypath+"/"+one_file, "r") as map_file :
        # print('Archivo actual', one_file)
        seed = int(map_file.readline())         #0
        # print("semilla",seed)
        # next(map_file)
        n_nodes = int(map_file.readline())      #1000
        # print("n nodos",n_nodes)
        # next(map_file)
        m_edges = int(map_file.readline())      #3809
        # print("aristas",m_edges)
        # next(map_file)
        b_description = map_file.readline()#0    
        # print("descripcion",b_description)
        # next(map_file)
        b_size = int(map_file.readline())       #1
        # print("nodos quemados size",b_size)
        # next(map_file)
        burn_nodes = int(map_file.readline())   #0
        # print("nodos Burn",burn_nodes)

        a_map = [ [0 for x in range(n_nodes)] for y in range(n_nodes)]

        for i in range(m_edges):
            xpos , ypos = tuple(map(int, map_file.readline().split(' ')))           # 1°
            # paralel matrix form the diagonal
            a_map[xpos][ypos] = 1
            a_map[ypos][xpos] = 1
    map_file.close()
    truemap = np.array(a_map)
    # myffp = ffp
    ffp.adjacency = truemap
    # print(ffp.size_of_graph)
    ffp.next_fire_set = {burn_nodes}
    ffp.ffp()
    results = open("results/results3.txt" , 'a')
    results.write(f'{one_file},{ffp.n_burned},{ffp.time_number},DL\n')
    # reseteo de valores
    ffp.burned_nodes.clear()
    ffp.n_burned = 0
    ffp.time_number = 0
    ffp.protected_nodes.clear()
    results.close()


'''
1 - tuple value from a string
https://www.geeksforgeeks.org/python-convert-string-to-tuple/

2 - Read one line from file
https://stackoverflow.com/questions/1904394/read-only-the-first-line-of-a-file

3 - Read n lines from file
https://stackoverflow.com/questions/1767513/how-to-read-first-n-lines-of-a-file
50_ep0.1_0_gilbert_1.in

'''