from copy import deepcopy
from time import time

# This file contains the implementation of Branch and bound


"""
This method is the helper method for calculating the branch and bound solution using recursion.
Inputs: 
    remaining_graph, num_nodes, current_index, partial_result, bestSol, start_time, cutoff_time, trace
"""
def helper(remaining_graph, num_nodes, current_index, partial_result, bestSol, start_time, cutoff_time, trace):
    # Define lower bound as the maximal matching for the corresponding subgraph
    # Input 
    #   graph: the remaining graph to calculate maximal matching
    def lower_bound(graph):
        graph = deepcopy(graph)
        counter = 0
        while len(graph.edges()) > 0:
            edge = list(graph.edges())[-1]
            graph.remove_nodes_from([edge[0],edge[1]])
            counter += 1
        return counter
    
    # Cutoff Branch and Bound for given time limit
    if time() > start_time + cutoff_time:
        raise RuntimeError
    # Check lower bound to prune
    curr_vc = len(partial_result)
    if curr_vc >= len(bestSol) - lower_bound(remaining_graph):
        return
    # Check if there are no more edges in remaining_graph
    elif len(remaining_graph.edges()) == 0:
        del bestSol[:]
        bestSol.extend(partial_result)
        trace.append(f"{round(time() - start_time, 2)}, {str(len(bestSol))}")
        return
    
    remaining_nodes = remaining_graph.nodes()
    # Expand the possible solutions
    for node in range(current_index, num_nodes + 1):
        if node not in remaining_nodes:
            continue
        expand_graph = deepcopy(remaining_graph)
        expand_graph.remove_node(node)
        helper(expand_graph, num_nodes, node + 1, partial_result + [node], bestSol, start_time, cutoff_time, trace)


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