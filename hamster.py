import networkx as nx # to make the graph
# import matplotlib.pyplot as plt
# import pandas as pd # to handle tabular data

G = nx.read_edgelist('web-Google.txt', create_using=nx.DiGraph(), nodetype=int)

print("Graph successfully created with", G.number_of_nodes(), "nodes and", G.number_of_edges(), "edges.")

# nx.draw(G)
# plt.show()