import networkx as nx # to make the graph
# import matplotlib.pyplot as plt
import pandas as pd # to handle tabular data

def main():
    subG = subGraphCreation()
    node_list = nodeListCreation(subG)
    apsp_calculation(subG)
    longestpath(subG, node_list)

def subGraphCreation():
    # creates the graph based off of Kaggle
    G = nx.read_edgelist('web-Google.txt', create_using=nx.DiGraph(), nodetype=int)
    print("Graph successfully created with", G.number_of_nodes(), "nodes and", G.number_of_edges(), "edges.")

    start_node = 123
    # Creates a subgraph from node 123 and with nodes with a depth of 5
    subG = nx.ego_graph(G, start_node, radius=5, center=True, undirected=False)
    print("Graph successfully created with", subG.number_of_nodes(), "nodes and", subG.number_of_edges(), "edges.")

    return subG

# Creates the list of nodes for the graph
def nodeListCreation(graph):
    node_list = list(graph.nodes())
    return node_list

def apsp_calculation(graph):
    
    paths = nx.all_pairs_shortest_path(graph)

    # turns paths into an easy list to turn into a dataframe and save to csv 
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

def longestpath(graph, node_list):

    allpaths = []

    # paths = nx.all_simple_paths(graph, source=node_list[0], target=node_list[5])
    # list_path = list(paths)
    # print(list_path)
    
    for node1 in node_list:
        for node2 in node_list:
            paths = nx.all_simple_paths(graph, source=node1, target=node2)
            list_path = list(paths)
            allpaths.append(list_path)

    print(f"path in index 5: {allpaths[5]}")
    print(f"path in index 13: {allpaths[13]}")
    
    maxLen = 0
    longestPathsList = []

    # for items in allpaths:
    #     if len(items) > maxLen:
    #         maxLen = len(items)
    #         longestPathsList.clear()
    #         longestPathsList.append(items)
    #     elif len(items) == maxLen:
    #         longestPathsList.append(items)

    print(f"Longest Path Length: {maxLen}")
    print(f"Longest Path Lists {longestPathsList}")


if __name__ == "__main__":
    main()




