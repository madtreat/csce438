# The purpose of this script is to display the results contained
# in the Crowdstorming SQLite Database in a clean, graphical manner.
#
# Created by Madison Treat, Kodi Tapie and Blake Robertson
#
#
# REQUIREMENTS TO DISPLAY:
#
# install numpy, matplotlib from sourceforge installers
# install networkx from pip
# install python-dateutil from pip
# install Graphviz from site
#
# pip uninstall pyparsing
# pip install -Iv https://pypi.python.org/packages/source/p/pyparsing/pyparsing-1.5.7.tar.gz#md5=9be0fcdcc595199c646ab317c1d9a709
# pip install pydot
# add C:\Program Files (x86)\Graphviz2.36\bin to path

#Reference this site for example: https://www.udacity.com/wiki/creating_network_graphs_with_python


import networkx as nx
import matplotlib.pyplot as plt
import sys, sqlite3


'''
query: FROM jobs SELECT Jobs_ID = JOB_ID (provided in command line)
    gets intital seed phrase
query: FROM hits SELECT Job_ID = JOB_ID
    gets every non-leaf node thats going to be in the graph - non_leaf_nodes
    
get level 0 node from non_leaf_node
make a hash table just for non-leaf-nodes
hash on hit_id, entry will be a (phrase, parent_hit_id):
for (int i=0; i<max_lvls; i++) {
    get all nodes at lvl=i
    foreach node at lvl = i
        parent_id = non-leaf-nodes-hash-table[node_hit_id][1]
        G.add_edge(non-leaf-nodes-hash-table[parent_id][0], non-leaf-nodes-hash-table[node_hit_id][0])
}
    
query: FROM results SELECT Job_ID = JOB_ID
    get every node thats going to be in the graph - all_nodes - stored in a list a tuples [(hit_id, task_id, response)]
    
    
select * from jobs where Jobs_ID = JOB_ID
'''

JOB_ID = sys.argv[1]
G = nx.Graph()

database = sqlite3.connect('crowdstorming.db')
db       = database.cursor()
db.execute("select Seed_Phrase from jobs where Job_ID = ?", [JOB_ID])
jobs_response = db.fetchall()
initial_seed_phrase = jobs_response[0][0]

db.execute("select * from hits where Job_ID = ?", [JOB_ID])
hits_response = db.fetchall()
# get max iter
max_iter = -1;
for rows in hits_response:
    if (int(rows[3]) > max_iter):
        max_iter = int(rows[3])
hits_set = {}
for rows in hits_response:
    hits_set[str(rows[1])] = (rows[5], rows[3])

iter_sorted_list = []
for i in range(0,max_iter+1):
    iter_sorted_list.append([])

for row in hits_response:
    iter_sorted_list[int(row[3])].append(row)

initial_node = str(iter_sorted_list[0][0][5])
G.add_node(initial_node)
for i in range(1,max_iter+1):
    for node in iter_sorted_list[i]:
        parent_id = node[2]
        G.add_edge(str(hits_set[str(parent_id)][0]), str(hits_set[str(node[1])][0]))

'''
for i in range(0,max_iter+1):
    for row in hits_response:
        if (int(row[3]) == i):
            parent_id = row[2]
            G.add_edge(hits_set[str(parent_id)],hits_set[str(row[1])])
    
db.execute('select * from results where Job_ID = ?', [JOB_ID])
results_response = db.fetchall()
for row in results_response:
    print row[3]

for i in range(0, len(results_response)):
    G.add_edge(hits_set[str(results_response[i][1])][0], str(results_response[i][3]))
'''
    
graph_pos = nx.pydot_layout(G)

graph_layout='shell'
node_size=1600
node_color='blue'
node_alpha=0.3
node_text_size=12
edge_color='blue'
edge_alpha=0.3
edge_tickness=1
edge_text_pos=0.3
text_font='sans-serif'
    
nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                       alpha=node_alpha, node_color=node_color)
nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                       alpha=edge_alpha,edge_color=edge_color)
nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                        font_family=text_font)


plt.show()
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

graph = [('Texas', 'cowboys'), ('Texas', 'boots'), ('Texas', 'lonestar'), ('Texas', 'big'), ('Texas', 'country')]



#draw_graph(graph)
'''