import networkx as nx
import matplotlib.pyplot as plt

# directed Graph
G = nx.DiGraph()
G.add_edges_from(
    [('1', '2'), ('1', '4'), 
     ('2', '3'), ('2', '6'), ('2', '5'),
     ('3', '6'), 
     ('4', '5'), ('4','7'),
     ('5', '6'), 
     ('6', '8'), ('6', '7'),
     ('7', '8'), ('7','9'),
     ('8','9')  ])

val_map = {'5':1.0}

values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
red_edges = [('5', '2'), ('5', '4')]
edge_colours = ['black' if not edge in red_edges else 'red'
                for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# # separate calls to draw nodes and edges
pos = nx.spring_layout(G)

nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), 
                       node_color = values, node_size = 500)
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
plt.show()