import matplotlib
matplotlib.use('TkAgg') # allow pop-up GUI

import networkx as nx # to make the graph
import pandas as pd # handle data
import matplotlib.pyplot as plt # graph visual 
import argparse # get arguments

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
    save_to_csv(data = {'path':paths_list}, filename = "apsp-123-5")

# Finds the longest *simple* path of the graph using DFS
def longestPaths(graph, node_list):
    longestPathList = []
    maxLen = 0
    numLongestPaths = 0

    # DFS initialization
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

# return closeness centrality list
def get_closeness_centrality(graph):
    n = len(graph)
    centrality = {}

    for node in graph.nodes:
        distances = nx.shortest_path_length(graph, target = node)
        total_distance = sum(distances.values())
        if total_distance > 0:
            centrality[node] = (n-1)/total_distance
        else:
            centrality[node] = 0

    return centrality

# save data to file
def save_to_csv(data, filename, columns = []):
    filename += ".csv"
    try:
        if columns:
            df = pd.DataFrame(data, columns = columns)
        else:
            df = pd.DataFrame(data)
        df.to_csv(filename, mode = "w", index = False)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise SystemExit(1)

# draw graph graph in spring layout, with most central node having a different color
def draw_graph(graph):
    # find most central node in graph
    closeness_centrality = nx.get_closeness_centrality(graph)
    most_central_node = max(closeness_centrality, key=closeness_centrality.get)

    # most central node is green and other nodes are pink
    node_colors = ["yellowgreen" if node == most_central_node else "pink" for node in graph]

    # draw, save, and show graph
    plt.figure(figsize = (9,8))
    nx.draw_spring(graph, arrows = True, with_labels = True, node_color = node_colors, node_size = 1500, font_size = 10)    # draw graph
    plt.savefig("graph.png")    # save graph as png
    plt.show()  # show pop-up GUI

# main function
def main():
    # process argument from command line
    parser = argparse.ArgumentParser(description = "This script read edge list from txt file and ...")
    
    parser.add_argument("filename", type = str, help = "Input file name (e.g., web-Google.txt)")
    parser.add_argument("-g", nargs=2, type = int, help = "Input integer fot start node and depth")
    parser.add_argument("-p", nargs=2, type = int, help = "Input integer for source and target node")

    args = parser.parse_args()

    # create initial graph
    try:
        graph = nx.read_edgelist(args.filename, create_using=nx.DiGraph(), nodetype=int)
    except FileNotFoundError:
        print("Error: file not found")
        raise SystemExit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise SystemExit(1)

    # no flag scenario: 
    # - save all pair shortest path and closeness centrality list for node start from 123 with depth of 5 in separate files
    # - output most central node
    # - output longest path
    if not args.g and not args.p:
        print("processing", args.filename)

        start_node = 123 #start at note 123
        depth = 5 #defined depth

        # subgraph start at note 123
        sub_graph = nx.ego_graph(graph, start_node, radius=depth, center=True, undirected=False)

        # calculate and save closeness centrality to file
        closeness_centrality = get_closeness_centrality(sub_graph)
        save_to_csv(closeness_centrality.items(), "closeness-123-5", ["node", "value"])
        print("created: closeness-123-5.csv")

        # process and save apsp to file
        apsp_calculation(sub_graph)
        print("created: apsp-123-5.csv")

        # find the node with the highest centrality
        most_central_node = max(closeness_centrality, key=closeness_centrality.get)
        print("most central node:", most_central_node)

        # find and print longest path
        node_list = nodeListCreation(sub_graph)
        longestPaths(sub_graph, node_list)

    # with -g: show sub graph starting at node with depth provided in arguments
    if args.g:
        if graph.has_node(args.g[0]):
            sub_graph = nx.ego_graph(graph, args.g[0], radius=args.g[1], center=True, undirected=False)
            draw_graph(sub_graph)
        else:
            print(f"Error: node {args.g[0]} is not in the graph")
            raise SystemExit(1)

    # with -p: output shortest path length from two given nodes
    if args.p:
        try:
            shortest_path = nx.shortest_path_length(graph, source=args.p[0], target=args.p[1])
            print(f"shortest path length from {args.p[0]} to {args.p[1]}: {shortest_path}")
        except nx.NodeNotFound:
            print(f"Error: node {args.p[0]} or {args.p[1]} are not in the graph")
            raise SystemExit(1)
        except nx.NetworkXNoPath:
            print(f"there is no patch from {args.p[0]} to {args.p[1]}")
        except nx.ValueError:
            print("Error: unsupported method")
            raise SystemExit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise SystemExit(1)

    raise SystemExit(0)

if __name__ == "__main__":
    main()