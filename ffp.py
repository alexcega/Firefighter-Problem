from numpy import genfromtxt
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

burned_nodes = []
protected_nodes = []
print('uno')

# Declare initial fire node
next_fire_set = {0}

# Read the graph from a csv file
mydata = genfromtxt('tree.csv', delimiter=',')

adjacency = mydata[1:,1:]
size_of_graph = len(adjacency)

# Colors inside graph
color_info = ['#00b4d9'] * size_of_graph


def updateColors():
    '''
    update the status of nodes, if burned -> red , if protected -> green
    '''
    for num in range(size_of_graph):
        if num in burned_nodes:
            color_info[num] = "#BD2000"
        if num in protected_nodes:
            color_info[num] = "green"

def show_graph_with_labels(adjacency_matrix):
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
    graph_colors = [color_map.get(node) for node in gr.nodes()]

    # print(color_info)
    # print(graph_colors)

    # fix position
    my_pos = nx.spring_layout(gr, seed=959595)
    
    nx.draw(gr, node_size=500,  pos = my_pos, node_color =graph_colors, labels=None, with_labels=True)
    # nx.draw_networkx_nodes(gr, node_size=500, pos=my_pos, node_color=graph_colors)
    plt.show()

def makeFire(next_fire_set, adjacency, burned_nodes):
    '''
    ## Burn adjacent nodes not protected
    '''
    update_next_fire = set()

    # Burn each node next to the fire if not protected
    for item in next_fire_set:
        if item not in protected_nodes:
            # Burn curr node
            burned_nodes.append(item)
            # Get update of next fire nodes (Neighbours)
            # In a set because you can access them from more than 1 edge but can't burn them twice
            for obj in updateNextFireNodes(next_fire_set,item, adjacency, burned_nodes) :
                update_next_fire.add(obj)
    return update_next_fire

def updateNextFireNodes(next_fire_set,curr_fire_node, adjacency, burned_nodes) :
    '''
    ## Get a list of Neighbours of curr fire node '''
    new_fire = []
    print(f"Current fire: {curr_fire_node}")
    for item in range(len(adjacency[curr_fire_node])) :
        if adjacency[curr_fire_node][item] == 1 : 
            if item not in burned_nodes and item not in protected_nodes:
                if item not in next_fire_set:
                    new_fire.append(item)
    print('Elements of new fire' , new_fire )
    print()
    return new_fire
    
def degreeGlobal() : 
    '''
    ## Degree
    Protect node with the highest amount of edges'''
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
    print('Nodo con mas conexiones es:',biggest_node_adj)
    protected_nodes.append(biggest_node_adj)
    return biggest_node_adj

def degreeLocal():
    '''
    ## Threat 
    Protect threated nodes
    Protect node with the highest amount of edges inside next_fire_set'''
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
    print('Nodo protegido local:', biggest_node_adj)
    protected_nodes.append(biggest_node_adj)
    return biggest_node_adj

visited_nodes = []

def countChildren(parentNode):
    '''
    ## Count the number of children in a parent node'''
    total_sons = [] # all of them, also grandchilds
    children_nodes = [] # only the direct sons
    for number in range(parentNode,size_of_graph):
        if number not in protected_nodes and number not in burned_nodes and parentNode not in visited_nodes:
            if adjacency[parentNode][number] == 1 : 
                children_nodes.append(number)
    # visited_nodes.append(parentNode)
    total_sons += children_nodes
    print("Padre", parentNode )
    print('hijos internos')
    print(total_sons)
    if len(children_nodes) > 0:
        for curr_node in children_nodes :
            total_sons += countChildren(curr_node)
    return total_sons

def biggestSubtree():
    '''
    ## Desc
    Get the node with the highest subtreee / sons'''
    biggest_child_node = -1
    total_children = 0
    for snode in next_fire_set:
        aux_count_child = countChildren(snode)
        if  len(aux_count_child) > total_children: 
            biggest_child_node = snode
            total_children = len(aux_count_child)

    if biggest_child_node != -1 : 
        print('Nodo con mas hijos:', biggest_child_node)
        print(f'Se protege {biggest_child_node}')
        protected_nodes.append(biggest_child_node)
        return biggest_child_node

    # en caso de ser un nodo default, no se entra en el try except de abajo
    elif len(next_fire_set) != 0 :
        default_node_to_save = next_fire_set.pop()
        print('Todos los nodos Son iguales, se proteje', default_node_to_save)
        protected_nodes.append(default_node_to_save)
        return default_node_to_save

    return biggest_child_node
        
def printStatus():
    print('Lista nodos por quemar', next_fire_set)
    print('Nodos ya quemados', burned_nodes)
    print('Nodos protegidos', protected_nodes)
    print()
    print("----------------------------------------")
    show_graph_with_labels(adjacency)

# Continuar hasta que todo el mapa este protegido/quemado
if __name__ == "__main__" : 
    time_number = 0
    while True :
        print(f" Iteracion numero #{time_number}")
        print()
        
        # Initialize number of firefighters / nodes to protect
        firefigthers_number = 1
        
        # Burn first node
        # Update next burning nodes
        next_fire_set = makeFire(next_fire_set, adjacency, burned_nodes)

        # Exit if
        # next_fire_set = 0 means fire can no longer extends
        if len(next_fire_set) == 0 :
            printStatus()
            break

        # Protect n nodes
        while firefigthers_number > 0:
            # Selected Heurisitc
            find_node_to_protect = biggestSubtree()

            firefigthers_number -= 1
            if find_node_to_protect == -1:
                break
            try:
                next_fire_set.remove(find_node_to_protect)
            except KeyError:
                pass

        # Exit if
        # next_fire_set = 0 means fire can no longer extends
        if len(next_fire_set) == 0 :
            printStatus()
            break

        printStatus()
        time_number += 1

    print(f'''
    Se termino el incendio, Tuvo una duracion de {time_number}s
    Se quemaron {len(burned_nodes)} nodos''')
    print(burned_nodes)
    print(f'Se protegieron {len(protected_nodes)} nodos')
    print(protected_nodes)

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