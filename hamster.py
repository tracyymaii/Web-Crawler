import networkx as nx # To make the graph
import pandas as pd # To handle tabular data

def main():
    subG = subGraphCreation()
    node_list = nodeListCreation(subG)
    if (nx.is_directed_acyclic_graph(subG)):
        isDag(subG)
    else:
        apsp_calculation(subG)
    longestPaths(subG, node_list)

# Creation of the subgraph based off of the original graph
def subGraphCreation():
    # Creates the graph based off of Kaggle
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

# Calculates the All Pairs Shortest Paths for the input graph
def apsp_calculation(graph):

    # Uses NetworkX All Pairs Shortest Path function to calculate all the shortest paths
    paths = nx.all_pairs_shortest_path(graph)

    # Turns paths into an easy list to turn into a dataframe and save to csv 
    paths_list = list(paths)
    df = pd.DataFrame({'path':paths_list})

    # Save to CSV
    df.to_csv("apsp-123-5.csv", index=False)

# Calculates the longest path if the input graph happens to be a directed acyclic graph
def isDag(graph):
    longestPath = nx.dag_longest_path(graph)
    longestPathLen = len(longestPath)

    print(f"Longest Path Length: {longestPathLen}")
    print(f"The Longest Path: {longestPath}")

# Finds the longest *simple* path of the graph using DFS
def longestPaths(graph, node_list):
    longestPathList = []
    maxLen = 0
    numLongestPaths = 0

    # DFS initialization by using a stack
    for start in node_list:
        stack = [(start, [start], set([start]))] # Current Node, Path, Visited Set

        while stack:
            node, path, visited = stack.pop()

            # Keeps track of the longest length, initial longest path, and 
            # number of paths with the same length as the longest length
            if len(path) > maxLen:
                maxLen = len(path)
                longestPathList.clear()
                longestPathList.append(path)
                numLongestPaths = 1
            elif len(path) == maxLen:
                numLongestPaths += 1

            for neighbor in graph.successors(node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], visited | {neighbor}))
    
    print(f"Longest Path Length: {maxLen}")
    print(f"Total Number of Paths with the Same Length: {numLongestPaths}")
    print(f"The First Longest Path: {longestPathList}")
            

if __name__ == "__main__":
    main()




