import argparse # get arguments

import networkx as nx # to make the graph
import pandas as pd # handle data

# graph visual and animation
import matplotlib
matplotlib.use('TkAgg') # allow pop-up GUI

import matplotlib.pyplot as plt
from matplotlib import animation

# Creates the list of nodes for the graph
def node_list_creation(graph):
    node_list = list(graph.nodes())
    return node_list

# Calculates the All Pairs Shortest Paths for the input graph
def apsp_calculation(graph):

    # Uses NetworkX All Pairs Shortest Path function to calculate all the shortest paths
    paths = nx.all_pairs_shortest_path(graph)

    # Turns paths into an easy list to turn into a dataframe and save to csv
    paths_list = list(paths)

    return paths_list

# Finds the longest *simple* path of the graph using DFS
def longest_paths(graph, node_list):
    longest_path_list = []
    max_len = 0
    num_longest_paths = 0

    # DFS initialization
    for start in node_list:
        stack = [(start, [start], set([start]))] # Current Node, Path, Visited Set

        while stack:
            node, path, visited = stack.pop()

            # Keeps track of the longest length, initial longest path, and
            # number of paths with the same length as the longest length
            if len(path) - 1 > max_len:
                max_len = len(path) - 1
                longest_path_list.clear()
                longest_path_list.append(path)
                num_longest_paths = 1
            elif len(path) - 1 == max_len:
                num_longest_paths += 1

            for neighbor in graph.successors(node):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], visited | {neighbor}))

    print(f"\nLongest Path Length: {max_len}")
    print(f"Total Number of Paths with the Same Length: {num_longest_paths}")
    print(f"The First Longest Path: {longest_path_list}")

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
def save_to_csv(data, filename, columns = None):
    filename += ".csv"
    try:
        if columns:
            df = pd.DataFrame(data, columns = columns)
            df.to_csv(filename, mode = "w", index = False)
        else:
            df = pd.DataFrame(data)
            df.to_csv(filename, mode = "w", index = False, header = False)
    except Exception as e:
      #  print(f"Unexpected error: {e}")
        raise SystemExit(f"Unexpected error: {e}")

# draw graph graph in spring layout, with most central node having a different color
def draw_graph(graph, graph_filename):
    ani_filename = graph_filename + ".gif"
    fig_filename = graph_filename + ".png"

    # animation
    fig, ax = plt.subplots(figsize = (9,8))
    edges = list(graph.edges())
    pos = nx.spring_layout(graph)

    # dynamic update
    def update(num):
        ax.clear()
        sub_graph = nx.DiGraph()
        sub_graph.add_edges_from(edges[: num + 1])

        sub_pos = {node: pos[node] for node in sub_graph.nodes()}

        # find most central node in graph
        closeness_centrality = get_closeness_centrality(sub_graph)
        most_central_node = max(closeness_centrality, key=closeness_centrality.get)

        # most central node is green and other nodes are pink
        node_colors = ["yellowgreen" if node == most_central_node else "pink" for node in sub_graph]

        nx.draw_networkx(sub_graph, pos = sub_pos, arrows = True, with_labels = True, node_color = node_colors, node_size = 1500, font_size = 10, ax = ax)

    if len(edges) > 0:
        try:
            ani = animation.FuncAnimation(fig = fig, func = update, frames = len(edges), interval = 500, repeat = False)
            ani.save(filename = ani_filename, writer = "pillow")
            plt.savefig(fig_filename)
            print(f"\nsaved:{ani_filename}")
        except Exception as e:
           # print(f"Unexpected error: {e}")
            raise SystemExit(f"Unexpected error: {e}")
    else:
        nx.draw_networkx(graph, pos = pos, with_labels = True, node_color = "yellowgreen", node_size = 1500, font_size = 10, ax = ax)
        plt.savefig(fig_filename)
        print("")

    print(f"saved:{fig_filename}")

    plt.show()

# main function
def main():
    # process argument from command line
    parser = argparse.ArgumentParser()

    parser.add_argument("filename", type = str, help = "Input file name (e.g., web-Google.txt)")
    parser.add_argument("-g", nargs=2, type = int, help = "Input integer for start node and depth")
    parser.add_argument("-p", nargs=2, type = int, help = "Input integer for source and target node")

    args = parser.parse_args()

    if not args.g and not args.p:
        # print("Error: no flag entered, atleast oone of -g or -p required")
        raise SystemExit("Error: no flag entered, atleast oone of -g or -p required")

    # create initial graph
    try:
        graph = nx.read_edgelist(args.filename, create_using=nx.DiGraph(), nodetype=int)
    except FileNotFoundError:
        # print("Error: file not found")
        raise SystemExit("Error: file not found")
    except Exception as e:
       # print(f"Unexpected error: {e}")
        raise SystemExit(f"Unexpected error: {e}")

    # no flag scenario:
    # - save all pair shortest path and closeness centrality list with provided start node and depth
    # - output most central node
    # - output longest path
    # - draw and show sub graph
    if args.g:
        if graph.has_node(args.g[0]):
            start_node = args.g[0]
            depth = args.g[1]

            suffix = "-" + str(start_node) + "-" + str(depth)
            
            closeness_filename = "closeness" + suffix
            apsp_filename = "apsp" + suffix
            graph_filename = "graph" + suffix

            sub_graph = nx.ego_graph(graph, start_node, radius=depth, center=True, undirected=False)
            
            # process and save apsp to file
            paths_list = apsp_calculation(sub_graph)
            save_to_csv(paths_list, apsp_filename)
            print(f"\ncreated: {apsp_filename}.csv")

            # calculate and save closeness centrality to file
            closeness_centrality = get_closeness_centrality(sub_graph)
            save_to_csv(closeness_centrality.items(), closeness_filename, ["node", "value"])
            print(f"created: {closeness_filename}.csv")

            # find the node with the highest centrality
            most_central_node = max(closeness_centrality, key=closeness_centrality.get)
            print("\nmost central node:", most_central_node)

            # find and print longest path
            node_list = node_list_creation(sub_graph)
            longest_paths(sub_graph, node_list)

            # draw graph
            draw_graph(sub_graph, graph_filename)
        else:
           # print(f"Error: node {args.g[0]} is not in the graph")
            raise SystemExit(f"Error: node {args.g[0]} is not in the graph")

    # with -p: output shortest path length from two given nodes
    if args.p:
        try:
            shortest_path = nx.shortest_path_length(graph, source=args.p[0], target=args.p[1])
            print(f"\nshortest path length from {args.p[0]} to {args.p[1]}: {shortest_path}")
        except nx.NodeNotFound:
          #  print(f"Error: node {args.p[0]} or {args.p[1]} are not in the graph")
            raise SystemExit(f"Error: node {args.p[0]} or {args.p[1]} are not in the graph")
        except nx.NetworkXNoPath:
            print(f"there is no patch from {args.p[0]} to {args.p[1]}")
        except Exception as e:
            # print(f"Unexpected error: {e}")
            raise SystemExit(f"Unexpected error: {e}")

    exit(0)

if __name__ == "__main__":
    main()
