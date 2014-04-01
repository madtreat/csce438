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
import matplotlib
import sys, sqlite3


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
for row in hits_response:
    if (int(row[3]) > max_iter):
        max_iter = int(row[3])
hits_set = {}
for row in hits_response:
    hits_set[str(row[1])] = (row[5], row[3])

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
        
# We aren't done yet, need to add outer most layer to graph
outer_hit_ids = []
for row in hits_response:
    if (int(row[3]) == max_iter):
        outer_hit_ids.append(str(row[1]))

# get results of those hit ids and add them to the graph
for hit_id in outer_hit_ids:
    db.execute("select Response from results where Hit_ID = ?", [hit_id])
    responses = db.fetchall()
    for phrase in responses:
        G.add_edge(str(hits_set[hit_id][0]), str(phrase[0]))

#for g in G:
#	print g
graph_pos = nx.pydot_layout(G)

graph_layout='shell'
node_size=0
node_color='blue'
node_alpha=0.3
node_text_size=15
node_text_color = 'black'
node_text_weight = 'bold'
edge_color='white'
edge_alpha=0.5
edge_tickness=2
edge_text_pos=0.3
text_font='sans-serif'

nx.draw_networkx_nodes(G,graph_pos,node_size=node_size, 
                       alpha=node_alpha, node_color=node_color,
					   ax=None)
nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                       alpha=edge_alpha,edge_color=edge_color,
					   ax=None)
nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                        font_family=text_font, font_color=node_text_color,
						font_weight=node_text_weight,
					   ax=None)

plt.axis('off')
plt.title('Crowdstorm: {}'.format(initial_seed_phrase))
plt.show()
