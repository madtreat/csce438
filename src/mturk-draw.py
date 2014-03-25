#install numpy, matplotlib from sourceforge installers
#install networkx from pip
#install python-dateutil from pip
#install Graphviz from site
#pip uninstall pyparsing
# pip install -Iv https://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.7.tar.gz#md5=9be0fcdcc595199c646ab317c1d9a709
# pip install pydot
# add C:\Program Files (x86)\Graphviz2.36\bin to path

#Reference this site for example: https://www.udacity.com/wiki/creating_network_graphs_with_python


import networkx as nx
import matplotlib.pyplot as plt



'''
Import table at given level shown below. Its values will correspond to the nodes/tables at next level
			seed
			  |
			 texas
		   /  |    \
	cowboys, dallas, rodeo		

'''

def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    G=nx.Graph()

    for edge in graph:
        G.add_edge(edge[0], edge[1])

    graph_pos = nx.pydot_layout(G)
    
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    # nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,label_pos=edge_text_pos)

    plt.show()

graph = [('dog',1),('dog',5),('dog',9),(1,2),(1,3),(1,4),(5,6),(5,7),(5,8),(9,10),(9,11),(9,12)]



draw_graph(graph)