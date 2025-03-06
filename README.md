[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/cVT3xsDh)
# Big Data Graph Analysis
Processing a BigData Graph with a third party library.

Read the PowerPoint on Canvas.
*You may use the Graph Library Shortest Paths functions*
*You **may not** use the Graph Library Closeness Centrality functions*
* You will work with the data available [here](https://www.kaggle.com/datasets/pappukrjha/google-web-graph/code).

**DO NOT COPY, DO THE PROJECT 100% YOURSELVES**

**USE AI AT YOUR OWN RISK**
> It is probable that I ask in the test about how you did something on this assignment, so learn very well!

## Introduction	
> Our program does various graph analyses on real data from Kaggle.
The graph that we analyze represent the connection of websites from one to another. We built our graph based off of a list of edges. From the data, we can determine that this is a directed unweighted graph. Our goal was to apply classroom computer science concepts and analyze how they scale to real-world data.

## Description -- Our Program Does the Following: 
### Builds the Neccessary Graphs to Analyze
> We used NetworkX, a graph library compatible with Python to build the original graph based off the Kaggle dataset. From there, we created a subgraph from node 123 including nodes it reached with a maximum depth of 5. This subgraph was created because  the following calculations would have taken up too much storage if it was done on the original graph.

### Calculates the All Pairs Shortest Paths
> The All Pairs Shortest Paths was calculated on the subgraph created and discussed earlier with a NetworkX function. These paths were turned into lists, to make it easier to turn into dataframes to format into a csv file. 

### Calculates the Longest Path
> We decided to calculate the longest path by running DFS from all the nodes. Originally, we planned on using NetworkX's simple path functions, however, decided to switch to DFS. More about our decision can be read below in "Reflection". 
>
> By using DFS, we are focusing on the longest simple path. DFS is optimal for calculating the longest path because it keeps track of the longest current path. This is very memory efficient. However, since we are focused on the finding the longest *simple* path, the caveat is that there is the possibility of the longest path having cycles, and this would go undetected by our program. 
>
>While doing DFS on the graph, once the entirety of a path has been traversed, its length is compared with the maximum length. If the current path is larger than the maximum length, then it will replace the maximum length and save the current path as the longest path. If the graph traverses more paths with the same length as the maximum length, it will add one to to the number of paths with the same maximum length. 

### Calculates the Shortest Path
> The shortest path is calculated based on the nodes from user input using a NetworkX function. These nodes are checked to ensure that they exist in the graph, and that there is a path between them. Then the length of the shortest path is outputted to the screen. Otherwise, an error message is outputted.

### Calculates Closeness Centrality
> Closeness Centrality is a measure of how close a node is to all other nodes. The node with a high closeness tends to be the one with the most inward adjacent edges.
>
> We calculated closeness centrality by first calculating the sum of the length of the shortest paths for each node. If the sum of the lengths of the shortest paths is 0, the so would the centrality of the node. Otherwise, the centrality of the node is calculated by the number of nodes minus one, divided by the sum of the lengths of the shortest path to that node. This process is repeated for the entirety of the list of nodes to find the closeness_centrality for all the nodes.

### Outputs a Graphical Representation of the Most Central Node
> After closeness centrality is calculated for the nodes on the graph, the most central node graph is created with the help of NetworkX and MatPlotLib. The center of the most central node graph is the node with the highest closeness centrality. This graph is output for users to see.
      
## Requirements	
> Device and application requirements for your program.
## User Manual
> Instructions for running your program.
## Reflection
> See “Reflection Requirements”

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
## Results
> Include screenshots of your program running.


