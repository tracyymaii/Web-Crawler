import networkx as nx # to make the graph
import pandas as pd # handle data

# get closeness centrality list
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

def save_to_csv(data, filename):
    df = pd.DataFrame(data.items(), columns=["node", "value"])
    df.to_csv(filename, index=False)


# load graph
G = nx.read_edgelist('web-Google.txt', create_using=nx.DiGraph(), nodetype=int)

start_node = 123 #start at note 123

# sub_nodes = list(nx.bfs_edges(G, source = start_node, depth_limit = 5))
# sub_nodes = set([start_node] + [v for u, v in sub_nodes])

# subG = G.subgraph(sub_nodes)

# subgraph start at note 123
subG = nx.ego_graph(G, start_node, radius=5, center=True, undirected=False)
closeness_centrality = nx.closeness_centrality(subG)
save_to_csv(closeness_centrality, "closeness-123-5.csv")

print("done!")

# print("Graph successfully created with", subG.number_of_nodes(), "nodes and", subG.number_of_edges(), "edges.")