import matplotlib
matplotlib.use('TkAgg') # allow pop-up GUI

import networkx as nx # to make the graph
import pandas as pd # handle data
import matplotlib.pyplot as plt # graph visual 
import argparse # get arguments

# return closeness centrality list
def closeness_centrality(G):
    n = len(G)
    centrality = {}

    for node in G.nodes:
        distances = nx.shortest_path_length(G, source = node)
        total_distance = sum(distances.values())
        if total_distance > 0:
            centrality[node] = (n-1)/total_distance
        else:
            centrality[node] = 0

    return centrality

# save data to file
def save_to_csv(data, filename, columns = []):
    if columns:
        df = pd.DataFrame(data.items(), columns = columns)
    else:
        df = pd.DataFrame(data.items())
    df.to_csv(filename, mode = "w", index = False)

# draw graph G in spring layout, with most central node having a different color
def draw_graph(G):
    # find most central node in G
    closeness_centrality = nx.closeness_centrality(G)
    most_central_node = max(closeness_centrality, key=closeness_centrality.get)

    # most central node is green and other nodes are pink
    node_colors = ["yellowgreen" if node == most_central_node else "pink" for node in G]

    # draw, save, and show graph
    plt.figure(figsize = (9,8))
    nx.draw_spring(G, arrows = True, with_labels = True, node_color = node_colors, node_size = 1500, font_size = 10)    # draw graph
    plt.savefig("graph.png")    # save graph as png
    plt.show()  # show pop-up GUI

# main function
def main():
    # process argument from command line
    parser = argparse.ArgumentParser(description = "This script read edge list from txt file and ...")
    
    parser.add_argument("filename", type = str, help = "Input file name (e.g., web-Google.txt)")
    parser.add_argument("-g", nargs=2, type = int, help = "")
    parser.add_argument("-p", nargs=2, type = int, help = "")

    args = parser.parse_args()

    # create initial graph
    G = nx.read_edgelist(args.filename, create_using=nx.DiGraph(), nodetype=int)

    # no flag scenario: 
    # - save all pair shortest path and closeness centrality list for node start from 123 with depth of 5 in separate files
    # - output most central node
    # - output longest path
    if not args.g and not args.p:
        print("processing", args.filename)

        start_node = 123 #start at note 123
        depth = 5 #defined depth

        # subgraph start at note 123
        subG = nx.ego_graph(G, start_node, radius=depth, center=True, undirected=False)

        # calculate and save closeness centrality to file
        closeness_centrality = nx.closeness_centrality(subG)
        save_to_csv(closeness_centrality, "closeness-123-5.csv", ["node", "value"])
        print("created: closeness-123-5.csv")

        # find the node with the highest centrality
        most_central_node = max(closeness_centrality, key=closeness_centrality.get)
        print("most central node:", most_central_node)

    # with -g: show sub graph starting at node with depth provided in arguments
    if args.g:
        print("drawing graph")
        subG = nx.ego_graph(G, args.g[0], radius=args.g[1], center=True, undirected=False)
        draw_graph(subG)
        print("done drawing")
    # with -p: output shortest path length from two given nodes
    if args.p:
        print("processing shortest path from", args.p[0], "to", args.p[1])
        shortest_path = nx.shortest_path_length(G, source=args.p[0], target=args.p[1])
        print("shortest path length from", args.p[0], "to", args.p[1], ":", shortest_path)


if __name__ == "__main__":
    main()