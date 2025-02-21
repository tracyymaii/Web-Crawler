import networkx as nx # to make the graph
import pandas as pd # to handle tabular data

# Nodes: 875713 Edges: 5105039

G = nx.DiGraph() # directed graph

# Read the file while ignoring comments
df_edges = pd.read_csv("web-Google.txt", sep = " ", comment = "#", header = None, names = ["FromNodeId", "ToNodeId"])

edges_list = list(df_edges.itertuples(index = False, name = None)) # index = false, excludes row index, name = none, regular tuples > named tuples

G.add_edges_from(edges_list)

print("Graph successfully created with", G.number_of_nodes(), "nodes and", G.number_of_edges(), "edges.")