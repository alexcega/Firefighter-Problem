from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

time_number = 0
burned_nodes = []
protected_nodes = []
n_burned =  0

adjacency = np.array([[0, 1, 1, 1, 0],[1, 0, 1, 0, 1],[1, 1, 0, 0, 0],[1, 0, 0, 0, 1],[0, 1, 0, 1, 0]])
size_of_graph= 0 
color_info = ['#00b4d9'] 

#* Declare initial fire node
next_fire_set = {0}

def auxResetValuess(burned_nodes,protected_nodes,):
    burned_nodes.clear()
    protected_nodes.clear()
    global n_burned, next_fire_set,time_number, color_info
    next_fire_set = {0}
    n_burned = 0
    time_number = 0
    color_info = ['#00b4d9'] 

def resetValues():
    auxResetValuess(burned_nodes,protected_nodes)

def startDataFromCSV(csv_file) : 
    # Read the graph from a csv file
    mydata = genfromtxt(csv_file, delimiter=',')
    global adjacency
    adjacency = mydata[1:,1:]

def updateColors():
    '''
    update the status of nodes, if burned -> red , if protected -> green
    '''
    for num in range(size_of_graph):
        if num in burned_nodes:
            color_info[num] = "#BD2000"
        if num in protected_nodes:
            color_info[num] = "green"

def showGraphWithLabels(adjacency_matrix):
    '''
    ## show graph of nodes protected and burned
    '''
    # get an update of colors in graph
    updateColors()
    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()

    gr.add_edges_from(edges)
    # asign color atribute to nodes
    for numero in range(size_of_graph):
        gr.nodes[numero]['color'] = color_info[numero]

    # dictionary of colors in graph
    color_map = nx.get_node_attributes(gr, 'color')
    graph_colors = [color_map.get(node,'#00b4d9' ) for node in gr.nodes()]

    # fix position
    my_pos = nx.spring_layout(gr, seed=959595)
    
    nx.draw(gr, node_size=400,  pos = my_pos, node_color =graph_colors, labels=None, with_labels=True)
    # nx.draw_networkx_nodes(gr, node_size=500, pos=my_pos, node_color=graph_colors)
    plt.show()

def makeFire(next_fire_set, adjacency, burned_nodes):
    '''
    ## Burn adjacent nodes not protected
    '''
    update_next_fire = set()

    #* Burn each node next to the fire if not protected
    for item in next_fire_set:
        if item not in protected_nodes:
            #* Burn curr node
            burned_nodes.append(item)
            #* Get update of next fire nodes (Neighbours)
            #* In a set because you can access them from more than 1 edge but can't burn them twice
            for obj in updateNextFireNodes(next_fire_set,item, adjacency, burned_nodes) :
                update_next_fire.add(obj)
    return update_next_fire

def updateNextFireNodes(next_fire_set,curr_fire_node, adjacency, burned_nodes) :
    '''
    ## Get a list of Neighbours of curr fire node 
    '''
    new_fire = []
    # print(f"Current fire: {curr_fire_node}")
    for item in range(len(adjacency[curr_fire_node])) :
        if adjacency[curr_fire_node][item] == 1 : 
            if item not in burned_nodes and item not in protected_nodes:
                if item not in next_fire_set:
                    new_fire.append(item)
    # print('Elements of new fire' , new_fire )
    # print()
    return new_fire
    
def degreeGlobal() : 
    '''
    ## Degree
    Protect node with the highest amount of edges
    '''
    # Nodo a proteger
    biggest_node_adj = -1
    # Cantidad de adjacencias
    total_adj = 0
    
    for i in range(len(adjacency)):
        if i  not in burned_nodes and i not in protected_nodes:
            aux_adj = 0
            for  j in range(len(adjacency[i])):
                if adjacency[i][j] == 1:
                    aux_adj += 1
            if aux_adj > total_adj : 
                total_adj = aux_adj
                biggest_node_adj = i
        # print(f'Nodo actual {i} con {aux_adj} conexciones')
    # print('Nodo con mas conexiones es:',biggest_node_adj)
    protected_nodes.append(biggest_node_adj)
    return biggest_node_adj

def degreeLocal():
    '''
    ## Threat 
    Protect threated nodes
    Protect node with the highest amount of edges inside next_fire_set
    '''
    biggest_node_adj = -1 
    total_adj = 0
    for node in next_fire_set:
        aux_adj = 0
        for j in range(size_of_graph):
            if adjacency[node][j] == 1:
                aux_adj += 1
        if aux_adj > total_adj:
            total_adj = aux_adj
            biggest_node_adj = node
    protected_nodes.append(biggest_node_adj)
    return biggest_node_adj

def countChildren(parentNode,visited_nodes):
    '''
    ## Count the number of children in a parent node
    '''
    
    total_elements_of_subtree = [] #* all of them
    children_nodes = [] #* only the direct sons

    for currNode in range(0,size_of_graph):
        if currNode not in burned_nodes: #* Dont visit parent
            if currNode not in visited_nodes: #* dont cicle inside triangules
                if adjacency[parentNode][currNode] == 1 : #* if there is a conection 
                    visited_nodes.append(currNode)
                    children_nodes.append(currNode)

    total_elements_of_subtree += children_nodes
    if len(children_nodes) > 0: #* check final level
        for visit_child in children_nodes : #* count the rest of the levels
            total_elements_of_subtree += countChildren(visit_child, visited_nodes)
    return total_elements_of_subtree

def biggestSubtree():
    '''
    ## Desc
    Get the node with the highest subtreee / sons
    '''
    biggest_child_node = -1
    total_children = 0
    for snode in next_fire_set:
        aux_count_child = countChildren(snode, [])
        if  len(aux_count_child) > total_children: 
            biggest_child_node = snode
            total_children = len(aux_count_child)

    if biggest_child_node != -1 : 
        # print('Nodo con mas hijos:', biggest_child_node)
        # print(f'Se protege {biggest_child_node}')
        protected_nodes.append(biggest_child_node)
        return biggest_child_node

    # en caso de ser un nodo default, no se entra en el try except de abajo
    elif len(next_fire_set) != 0 :
        default_node_to_save = next_fire_set.pop()
        # print('Todos los currNode Son iguales, se proteje', default_node_to_save)
        protected_nodes.append(default_node_to_save)
        return default_node_to_save

    return biggest_child_node
        
def countGrandChildren(parentNode,visited_nodes, limit):
    '''
    ## Count the number of children in a parent node with a specifc limit
    '''
    total_elements_of_subtree = [] #* all of them, also grandchilds
    children_nodes = [] #* only the direct sons
    if ( limit  > 0 ) :
        for currNode in range(0,size_of_graph):
            if currNode not in burned_nodes: #* no ir hace arriba
                if currNode not in visited_nodes: #* no repetir triangulos
                    if adjacency[parentNode][currNode] == 1 : #* si si hay conexion 
                        visited_nodes.append(currNode)
                        children_nodes.append(currNode)

        total_elements_of_subtree += children_nodes
        if len(children_nodes) > 0:
            for visit_child in children_nodes :
                total_elements_of_subtree += countGrandChildren(visit_child, visited_nodes, limit-1)
    return total_elements_of_subtree


def biggestGrandChildren():
    '''
    ## BGC
    Get the node with the highest subtreee / sons at a limit '''
    biggest_family = -1
    total_children = 0
    for snode in next_fire_set:
        aux_count_child = countGrandChildren(snode, [] , 2)
        if  len(aux_count_child) > total_children: 
            biggest_family = snode
            total_children = len(aux_count_child)

    if biggest_family != -1 : 
        # print('Nodo con mas nietos:', biggest_child_node)
        # print(f'Se protege {biggest_child_node}')
        protected_nodes.append(biggest_family)
        return biggest_family

    # en caso de ser un nodo default, no se entra en el try except de abajo
    elif len(next_fire_set) != 0 :
        default_node_to_save = next_fire_set.pop()
        # print('Todos los currNode Son iguales, se proteje', default_node_to_save)
        protected_nodes.append(default_node_to_save)
        return default_node_to_save

    return biggest_family

def printStatus():
    showGraphWithLabels(adjacency)
    print('Lista currNode por quemar', next_fire_set)
    print('currNode ya quemados', burned_nodes)
    print('currNode protegidos', protected_nodes)
    print()
    print("----------------------------------------")
    

# Continuar hasta que todo el mapa este protegido/quemado

def ffp(heuristic, info) :
    global size_of_graph , color_info

    size_of_graph = len(adjacency)

    #^ Colors inside graph
    color_info = ['#00b4d9'] * size_of_graph
    global time_number
    
    while True :
        # print(f" Iteracion numero #{time_number}")
        # print()
        
        #^ Initialize number of firefighters / nodes to protect
        firefigthers_number = 1
        
        #^ Burn first node
        #^ Update next burning nodes
        global next_fire_set
        next_fire_set = makeFire(next_fire_set, adjacency, burned_nodes)

        #^ Exit if
        #* next_fire_set = 0 means fire can no longer extends
        if len(next_fire_set) == 0 :
            if info : printStatus()
            break

        #^ Protect n nodes
        while firefigthers_number > 0:
            # Selected Heurisitc
            find_node_to_protect = heuristic()

            firefigthers_number -= 1
            if find_node_to_protect == -1:
                break
            try:
                next_fire_set.remove(find_node_to_protect)
            except KeyError:
                pass

        #^ Exit if
        #* next_fire_set = 0 means fire can no longer extends
        if len(next_fire_set) == 0 :
            if info: printStatus()
            break

        if info : printStatus()
        time_number += 1


    global n_burned
    n_burned = len(burned_nodes)
    # print(
    # f'''Se termino el incendio, Tuvo una duracion de {time_number}s\nSe quemaron {n_burned} currNode''')
    # print(burned_nodes)
    # print(f'Se protegieron {len(protected_nodes)} currNode')
    # print(protected_nodes)    
    
    # print("******************************")

startDataFromCSV('mapslocal/10_local_80g_30p_8-10_9False.txt')
ffp(biggestGrandChildren, True)


'''
Color nodes
https://stackoverflow.com/questions/27030473/how-to-set-colors-for-nodes-in-networkx
fix position :
https://stackoverflow.com/questions/69303984/networkx-is-plotting-different-graph-each-time
Color nodes by atribute
https://www.youtube.com/watch?v=SiXjTkGFwng&ab_channel=PythonTutorialsforDigitalHumanities
Set atribute to nodes
https://stackoverflow.com/questions/13698352/storing-and-accessing-node-attributes-python-networkx
'''