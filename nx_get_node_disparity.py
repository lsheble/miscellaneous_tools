# NODE DISPARITY (Y2)
# For each node, extract the disparity of edge weight distribution across nodes to which the focal node is connected
# need strength of edges from each node
# see, e.g., Miritello G, Moro E, Lara R, Martinez R, Belchamber J, Roberts S, Dunbar R (2012) Time as a
# limited resource: communication strategy in mobile phone networks. Social Networks 35, 89–95. doi: 10.1016/j.socnet.2013.01.003
#
# Ysub i = sum of (weight (ij edge)/strength (i node))^2, 
# from j=1 to j=k sub i
# where w sub ij = weight of the edge between i and j,
#       s sub i = sum of weight of all edges from i (aka 'node strength')
#       k sub i = 'connectivity', here, just the number of edges to other nodes
# note: node disparity = 1 is most disparate; = 0 is least
#
# https://plot.ly/~sheble/4/

import networkx as nx

def get_node_disparity(G, node):
    node_strength = nx.degree(G, node, weight='weight')
    disparity = 0
    for neighbor in nx.all_neighbors(G,node):
        wt = float(G.edge[node][neighbor]['weight'])
        wt_strength = (wt/node_strength)
        wt_str_sq = (wt_strength)*(wt_strength)
        disparity += wt_str_sq
    return disparity
