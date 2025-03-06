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
> Introduce your program. What’s the point of the project?

Our program does various graph analyses on real data from Kaggle.
The graph that we analyze represent the connection of websites from one to another. We built our graph based off of a list of edges. From the data, we can determine that this is a directed unweighted graph.

## Description
> Describe what your program does. Also describe closeness centrality and how you implemented it. Remember to include snipets of code in your explanation. (Is it possible to link to your actual code?)

Our program does the following: 
    - Builds a graph using NetworkX based off of the list of edges from 
      the Kaggle
    - 
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


