# Big Data Graph Analysis
Processing a BigData Graph with a third party library.

## Introduction	
> Our program does various graph analyses on real data from Kaggle.
The graph that we analyze represent the connection of websites from one to another. We built our graph based off of a list of edges. From the data, we can determine that this is a directed unweighted graph. Our goal was to apply classroom computer science concepts and analyze how they scale to real-world data.

## Description -- Our Program Does the Following: 
### Builds the Neccessary Graphs to Analyze
> We used NetworkX, a graph library compatible with Python to build the original graph based off the Kaggle dataset. From there, we created a subgraph based on user input. The user can input the start node and the maximum depth from the start node. All nodes that can be reached by the start node and this depth will be used to create the subgraph. This subgraph was created because the following calculations would have taken up too much storage if it was done on the original graph.

### Calculates the All Pairs Shortest Path
> The All Pairs Shortest Path function from NetworkX calculates the shortest paths between all nodes. This was done on the subgraph created and discussed earlier. These paths are turned into lists, to make it easier to turn into dataframes to format into a csv file. 

### Calculates the Longest Path
> One of the easiest ways to calculate the longest path is if the graph is a directed acyclic graph. This is the first thing that we check for when calculating the longest path. If the graph is not a DAG, then we do the following.
>
>We decided to calculate the longest path by running DFS from all the nodes. Originally, we planned on using NetworkX's simple path functions, however, decided to switch to DFS. More about our decision can be read below in "Reflection".
>
> By using DFS, we are focusing on the longest simple path. DFS is optimal for calculating the longest path because it keeps track of the longest current path. This is very memory efficient. However, since we are focused on the finding the longest *simple* path, the caveat is that there may exist a longest path that contains cycles or revisits nodes, and this would go undetected by our program. 
>
>While doing DFS on the graph, once the entirety of a path has been traversed, its length is compared with the maximum length. If the current path is larger than the maximum length, then it will replace the maximum length and save the current path as the longest path. If the graph traverses more paths with the same length as the maximum length, it will add one to to the total number of paths with the same maximum length. 

### Calculates the Shortest Path
> The shortest path is calculated with a NetworkX function, between two nodes given by the user. These nodes are checked to ensure that they exist in the graph, and there exists a path between them. Then the length of the shortest path is outputted to the screen. Otherwise, an error message is outputted.

### Calculates Closeness Centrality
> Closeness Centrality is a measure of how close a node is to all other nodes. The node with a high closeness centrality tends to be the one with the most incoming edges, compared to the other nodes in the graph.
>
> We calculated [closeness centrality](./mango.py) by first calculating the sum of the lengths of the shortest paths for each node. If the sum of the lengths of the shortest paths from that node is 0, the closeness centrality of the node would be 0 as well. Otherwise, the centrality of the node is calculated by the number of nodes minus one, divided by the sum of the lengths of the shortest paths from that node to all the nodes. This process is repeated for the entirety of the nodes in the graph to find the closeness centrality for all the nodes.

```
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
```

### Outputs a Graphical Representation of the Most Central Node
> After closeness centrality is calculated for every node in the graph, the most central node graph is created with the help of NetworkX and MatPlotLib. The graph shows the most central node, and all of its incoming edges. The center of the most central node graph is colored differently, highlighting the node with the highest closeness centrality. This graph is outputted for users to see.
      
## Requirements	
> Our Requirements file, requirements.txt, shows everything that is necessary to run our program, libraries, etc. The user manual will go over how to use the requirements file in order to run out program.
>
> After testing the program on both of our relatively slow computers, running the entire program and all of it functions can take anywhere from ___ TIME to ____ TIME depending on the size of the graph and each computer system itself. We recommend setting at least this amount of time aside to run our program, and to watch anime whilst waiting. 

## User Manual
> Program runs in WSL Ubuntu:
>
> **1.** Install dependencies from `requirements.txt`
>```
>pip install -r requirements.txt
>```
> **2.** Install `tk` to support interactive plotting
>```
>sudo apt install python3-tk
>```
> **3.** Run `yolkie.py` with a `.txt` file of graph's edge list and `-g` and/or `-p`
>```
>python3 yolkie.py <graph-edges>.txt -g <start-node> <depth> -p <source-node> <target-node>
>```

## Reflection
> While completing this assignment, the algorithms that took the longest time for us to figure out were calculating the longest path and the closeness centrality.
>
> The original graph that we received is a directed graph, however, it is not acyclic. The likelihood of there being a directed acyclic subgraph from the user input is small, however, not impossible. 
>
> Originally, to find the longest path of a directed non-acyclic graph, we were going to find the all simple paths of that graph. Then we would find the maximum path from there and return it. After attempting to run this code for two seperate 4 hours sessions, where the code never completed running, we decided that it was most likely not the most optimal solution. While finding a *single* path using NetworkX's function can be done in $O(n+m)$ time, finding *all* the simple paths can take up to $O(n!)$ when the graph has many simple paths. 
> 
> NetworkX's all simple paths function, naturally stores all the simple paths at the same time. This is very space inefficient since we only care about the longest path. In an attempt to optimize the funcion we focused on only keeping track of the longest path with a nested for loop. However, this step took an additional nested $O(n)$ time, making our runtime much much worst. It was after facing these difficulties that we brainstormed and decided on DFS. 
>
> Prior to this assignment, we did not know what closeness centrality was. So we started by researching closeness centrality, to ensure that we had a full understanding of the algorithm before we began to code. We did so by reading Wikipedia, turning to YouTube, and talking to fellow classmates. Closeness centrality can be used to explain how close a node is to other nodes in the graph. If the node has a higher closeness centrality it is more central, and therefore has a higher number of incoming edges compared to other nodes in the graph.
>
> Closeness centrality is calculated by taking the number of nodes minus one and dividing it by the sum of the shortest path lengths from that node to all other nodes. A more detailed explanation of the algorithm can be found in the "Description" portion of this readme. To get all of the shortest path lengths from a single node to all other nodes, we used the shortest path length function from NetworkX. Then took the sum of those values to calculate the total distance. Getting the shortest path lengths takes $O(n+m)$ time due to NetworkX's implementation of [shortest path length](https://networkx.org/documentation/stable/_modules/networkx/algorithms/shortest_paths/generic.html#shortest_path_length) with [BFS](https://networkx.org/documentation/stable/_modules/networkx/algorithms/shortest_paths/unweighted.html#single_source_shortest_path_length) when the graph is unweighted, which ours is. While this is not explicitly stated on their website, it is present in their source code. Then, this process is repeated for all of the nodes in the graph, resulting in another $O(n)$ time. The total time complexity is $O(n*(n+m))$, approximately, $O(n^2)$. 


## Results
> Include screenshots of your program running.


