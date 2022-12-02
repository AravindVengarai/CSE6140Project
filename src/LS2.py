# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 13:41:17 2022

@author: AlecF
"""
import time
import random
import copy        
            
def ConstructVC(inputGraph):
    C = list()
    for u, v in inputGraph.edges():
        inputGraph.edges()[u, v]['covered'] = False
    for u,v in inputGraph.edges():
        if inputGraph.edges()[u,v]['covered'] == False:
            C.append(u)
            for a in inputGraph.adj[u]:
                inputGraph.edges()[u, a]['covered'] = True
    return C
        

def Cost(graph, v):
    cost = 0
    if v >= 0:
        for a in graph.adj[v]:
            cost = cost + 1
    return cost

def dscore(graph, C, v):
    firstCost = Cost(graph, -1)

    secondCost = Cost(graph,v)
    dscore = firstCost - secondCost
    return dscore

def local_search_2(inputGraph, cutoffTime, seed):
    random.seed(seed)

    startTime = time.time()

    # sol is the solution list returned by the algorithm
    sol = list()
    # trace keeps track of solutions at different time points
    trace = list()
    
    C = list()
    
    numEdges = inputGraph.size()
    gamma = 0.5*len(inputGraph)
    rho = 0.3

    # Add a covered attribute to each of the edges
    for u, v in inputGraph.edges():
        inputGraph.edges()[u, v]['covered'] = False
        inputGraph.edges()[u, v]['weight'] = 1
        

    # Initialize dscore, age, confChange for each vertex
    for vertex in inputGraph.nodes():
        inputGraph.nodes()[vertex]['dscore'] = dscore(inputGraph, C, vertex)
        inputGraph.nodes()[vertex]['age'] = 0
        inputGraph.nodes()[vertex]['confChange'] = 1
    
    # Create initial C
    C = ConstructVC(inputGraph)
    sol = copy.deepcopy(C)
    covered = True
    
    while (time.time() - startTime < cutoffTime) and (len(C) > 0):
        
        if covered:
            maxVertexValue = inputGraph.nodes()[C[0]]['dscore']
            maxVertex = C[0]
            for c in C:
                if inputGraph.nodes()[c]['dscore'] > maxVertexValue:
                    maxVertex = c
                    maxVertexValue = inputGraph.nodes()[c]['dscore']
                    
            vertexChoices = []
            for c in C:
                 if inputGraph.nodes()[c]['dscore'] == maxVertexValue:
                     vertexChoices.append(c)
            
            choice = random.randint(0,len(vertexChoices)-1)
            maxVertex = vertexChoices[choice]

            C.remove(maxVertex)
            inputGraph.nodes()[maxVertex]['age'] = 0
            
            for u, v in inputGraph.edges():
                inputGraph.edges()[u,v]['covered'] = False
                if (C.count(u) > 0):
                    for a in inputGraph.adj[u]:
                        inputGraph.edges()[u, a]['covered'] = True
                elif (C.count(v) > 0):
                    for a in inputGraph.adj[v]:
                        inputGraph.edges()[v, a]['covered'] = True

        uncovered = []
        
        for u,v in inputGraph.edges():
            if inputGraph.edges()[u, v]['covered'] == False:
                uncovered.append([u, v])
        if len(uncovered) > 0:
            
            maxVertexValue = inputGraph.nodes()[C[0]]['dscore']
            maxVertex = C[0]
            for c in C:
                if inputGraph.nodes()[c]['dscore'] > maxVertexValue:
                    maxVertex = c
                    maxVertexValue = inputGraph.nodes()[c]['dscore']
                    
            vertexChoices = []
            for c in C:
                 if inputGraph.nodes()[c]['dscore'] == maxVertexValue:
                     vertexChoices.append(c)
            
            maxAge = inputGraph.nodes()[vertexChoices[0]]['age']
            for ch in vertexChoices:
                if inputGraph.nodes()[ch]['age'] > maxAge:
                    maxAge = inputGraph.nodes()[ch]['age']
                    maxVertex = ch

            C.remove(maxVertex)
            inputGraph.nodes()[maxVertex]['age'] = 0
            inputGraph.nodes()[maxVertex]['confChange'] = 0
            for a in inputGraph.adj[maxVertex]:
                inputGraph.nodes[a]['confChange'] = 1
            
            # Choose an uncovered edge at random
            choice = random.randint(0,len(uncovered)-1)
            chosenEdge = uncovered[choice]
            if (inputGraph.nodes()[chosenEdge[0]]['confChange'] == 1) and (inputGraph.nodes()[chosenEdge[1]]['confChange'] == 1):
                if (inputGraph.nodes()[chosenEdge[0]]['dscore']) > (inputGraph.nodes()[chosenEdge[1]]['dscore']):
                    selection  = chosenEdge[0]
                else:
                    selection  = chosenEdge[1]
            else:
                if (inputGraph.nodes()[chosenEdge[0]]['confChange'] == 1):
                   selection  = chosenEdge[0]
                else:
                    selection  = chosenEdge[1]
            C.append(selection)

            for a in inputGraph.adj[selection]:
                inputGraph.nodes()[a]['confChange'] = 1
            
            # Assume graph is covered and check below 
            covered = True
                
            # Set all edges to uncovered, update covered edges, add 1 to the weight of each uncovered edge
            for u, v in inputGraph.edges():
                inputGraph.edges()[u,v]['covered'] = False
                if (C.count(u) > 0):
                    for a in inputGraph.adj[u]:
                        inputGraph.edges()[u, a]['covered'] = True
                elif (C.count(v) > 0):
                    for a in inputGraph.adj[v]:
                        inputGraph.edges()[v, a]['covered'] = True
                else:
                    inputGraph.edges()[u,v]['weight'] = inputGraph.edges()[u,v]['weight'] + 1
                
                # If any edge is not covered set covered to False
                if inputGraph.edges()[u,v]['covered'] == False:
                    covered = False
            

            totalWeight = 0
            for u, v in inputGraph.edges():
                totalWeight = totalWeight + inputGraph.edges()[u,v]['weight']
            avgWeight = totalWeight/numEdges
            if avgWeight > gamma:
                for u, v in inputGraph.edges():
                    inputGraph.edges()[u,v]['weight'] = rho*inputGraph.edges()[u,v]['weight']
                    
            for c in C:
                inputGraph.nodes()[c]['age'] = inputGraph.nodes()[c]['age'] + 1
        
        if covered:
            sol = copy.deepcopy(C)
            trace.append((time.time() - startTime, len(C)))
            
            
    return sol, trace
