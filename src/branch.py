from copy import deepcopy
from time import time

# This file contains the implementation of Branch and bound


"""
This method is the helper method for calculating the branch and bound solution using recursion.
Inputs: 
    remaining_graph, num_nodes, current_index, partial_result, bestSol, start_time, cutoff_time, trace
"""
def helper(remaining_graph, num_nodes, current_index, partial_result, bestSol, start_time, cutoff_time, trace):
    # Cutoff Branch and Bound for given time limit
    if time() - start_time > cutoff_time:
        raise RuntimeError

    # Define lower bound as the number of edges generated from a maximal matching
    # Input 
    #   graph: the remaining graph to calculate maximal matching
    def lower_bound(graph):
        lower_b = 0
        graph = deepcopy(graph)
        while list(graph.edges()) != []:
            edge = list(graph.edges())[-1]
            graph.remove_nodes_from([edge[0],edge[1]])
            lower_b = lower_b + 1
        return lower_b
    
    # Check lower bound to prune
    if len(partial_result) + lower_bound(remaining_graph) >= len(bestSol):
        return
    # Check if there are no more edges in remaining_graph
    elif list(remaining_graph.edges()) == []:
        del bestSol[:]
        for node in partial_result:
            bestSol.append(node)
        trace.append(f"{round(time() - start_time, 2)}, {str(len(bestSol))}")
        return
    
    remaining_nodes = remaining_graph.nodes()
    # Expand the possible solutions
    for node in range(current_index, num_nodes + 1):
        if node not in remaining_nodes:
            continue
        partial_result.append(node)
        expand_graph = deepcopy(remaining_graph)
        expand_graph.remove_node(node)
        helper(expand_graph, num_nodes, node + 1, partial_result, bestSol, start_time, cutoff_time, trace)
        del partial_result[-1]


"""
This method contains the intiailization and starting call for the branch and bound solution.
Inputs: 
    graph:          the graph to calculate minimum vertex cover over
    cutoff_time:    the cutoff time to perform search over
Outputs:
    bestSol:        the best solution found from branch and bound
    bestSolTrace::  trace of the best found solution along with time found
"""
def branch_and_bound(graph, cutoff_time):
    bestSol = list(graph.nodes())
    num_nodes = len(bestSol)

    # Initialize trace and partial result tracker
    bestSolTrace = []
    partial_result = []

    try:
        helper(graph, num_nodes, 1, partial_result, bestSol, time(), cutoff_time, bestSolTrace)
    except RuntimeError:
        print(f"Algorithm timeout after {cutoff_time} seconds")
    
    return bestSol, bestSolTrace