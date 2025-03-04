import networkx as nx # to make the graph
# import matplotlib.pyplot as plt
import pandas as pd # to handle tabular data

# creates the graph based off of Kaggle
G = nx.read_edgelist('web-Google.txt', create_using=nx.DiGraph(), nodetype=int)
print("Graph successfully created with", G.number_of_nodes(), "nodes and", G.number_of_edges(), "edges.")


start_node = 123
# Creates a subgraph from node 123 and with nodes with a depth of 5
subG = nx.ego_graph(G, start_node, radius=5, center=True, undirected=False)
print("Graph successfully created with", subG.number_of_nodes(), "nodes and", subG.number_of_edges(), "edges.")

def apsp_calculation(graph):
    paths = nx.all_pairs_shortest_path(graph)

    paths_list = list(paths)
    df = pd.DataFrame({'path':paths_list})

    # Save to CSV
    df.to_csv("apsp-123-5.csv", index=False)

# must find all simple paths, and find the longest path from there
# because if we attempt to just find the longest path directly, it will not work since the graph has cycles

# for all simple paths,
# use networkx to get all simple paths
# but then keep a counter for the max length,
# and another data structure for the paths
# then if the cur path len is = the cur max len
# then add it to the data structure
# if the cur path len is > cur max len  
# empty the data structure
# then add the curr path to the structure

def longest(graph):
    longest_path = nx.dag_longest_path(graph)
    longest_path_len = nx.dag_longest_path_length(graph)
    print(f"longest Path Length: {longest_path_len}\n")
    print(f"longest Actual Path: {longest_path}\n")

apsp_calculation(subG)
# longest(subG)