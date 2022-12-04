from copy import deepcopy
from time import time
import operator
from math import ceil
import networkx as nx

# This file contains the implementation of Branch and bound


"""
This method is the helper method for calculating the branch and bound solution using recursion.
Inputs: 
    remaining_graph, num_nodes, current_index, partial_result, bestSol, start_time, cutoff_time, trace
"""
def helper(graph, partial_result, bestSol, start_time, cutoff_time, trace, deglist_sorted):
    # Define lower bound as the maximal matching for the corresponding subgraph
    # Input 
    #   graph: the remaining graph to calculate maximal matching
    def lower_bound(graph, nodes):
        graph = graph.subgraph(nodes)
        graph = nx.Graph(graph)
        counter = 0
        while len(graph.edges()) > 0:
            edge = list(graph.edges())[-1]
            graph.remove_nodes_from([edge[0],edge[1]])
            counter += 1
        return counter
    
    # def order(graph, nodes):
    #     graph = graph.subgraph(nodes)
    #     deglist = graph.degree()
    #     deglist_sorted = sorted(deglist, key=operator.itemgetter(1))
    #     return deglist_sorted
        # v = deglist_sorted[0] 
        # return v[0]
        # lb = graph.number_of_edges() / v[1]
        # return ceil(lb)

    # Cutoff Branch and Bound for given time limit
    if time() > start_time + cutoff_time:
        raise RuntimeError

    def check_solution(graph, exis_sol):
        graph = deepcopy(graph)
        graph.remove_nodes_from(exis_sol)
        return len(graph.edges()) == 0
    
    stillVertexCover = check_solution(graph, partial_result)
    if not stillVertexCover:
        return
    
    # Check lower bound to prune
    curr_vc = len(partial_result)
    
    # if curr_vc > len(bestSol):
    #     return
    
    if lower_bound(graph, partial_result) >= len(bestSol):
        return

    if len(partial_result) < len(bestSol):
        del bestSol[:]
        bestSol.extend(partial_result)
        trace.append((round(time() - start_time, 2), len(bestSol)))
    # Check if there are no more edges in remaining_graph
    # if len(remaining_graph.edges()) == 0:
    #     exis_sol = len(bestSol)
    #     for _ in range(exis_sol):
    #         bestSol.pop()
    #     bestSol.extend(partial_result)
    #     trace.append(f"{round(time() - start_time, 2)}, {str(len(bestSol))}")
    #     return
    
    # order_nodes = order(graph, partial_result)
    # Expand the possible solutions
    for idx, (vertex, degree) in enumerate(deglist_sorted):
        deglist_pass = deepcopy(deglist_sorted)
        deglist_pass.pop(idx)
        new_result = deepcopy(partial_result)
        new_result.remove(vertex)
        helper(graph, new_result, bestSol, start_time, cutoff_time, trace, deglist_pass)


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
    deglist = graph.degree()
    deglist_sorted = sorted(deglist, key=operator.itemgetter(1))

    # Initialize trace and partial result tracker
    bestSolTrace = []
    partial_result = list(graph.nodes())

    try:
        helper(graph, partial_result, bestSol, time(), cutoff_time, bestSolTrace, deglist_sorted)
    except RuntimeError:
        print(f"Algorithm timeout after {cutoff_time} seconds")
    
    return bestSol, bestSolTrace