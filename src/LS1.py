import time
import random
import numpy as np
import copy


def local_search_1(inputGraph, cutoffTime, seed):
    random.seed(seed)

    startTime = time.time()

    # sol is the solution list returned by the algorithm
    sol = list()
    # trace keeps track of solutions at different time points
    trace = list()

    # Add a covered attribute to each of the edges
    for u, v in inputGraph.edges():
        inputGraph.edges()[u, v]['covered'] = False

    # Initialize gain and loss for each vertex
    for vertex in inputGraph.nodes():
        inputGraph.nodes()[vertex]['loss'] = np.inf
        inputGraph.nodes()[vertex]['gain'] = 0
        inputGraph.nodes()[vertex]['age'] = 0

    # Create initial C
    C = ConstructVC(inputGraph)

    # Loops until time cutoff is reached
    while (time.time() - startTime < cutoffTime) and (len(C) > 0):
        for vertex in inputGraph.nodes():
            inputGraph.nodes()[vertex]['age'] += 1

        # Check if C covers all edges
        # An edge is marked as covered iff C currently covers it
        allEdgesCovered = True
        for u, v in inputGraph.edges():
            if inputGraph.edges()[u, v]['covered'] == False:
                allEdgesCovered = False
                break

        # A solution has been found (will keep looking for a more optimal one)
        if allEdgesCovered == True:
            sol = copy.deepcopy(C)
            trace.append((time.time() - startTime, len(C)))

            # Get the vertex with the lowest loss value
            # [0] at the end selects the vertex value rather than an attribute
            minVertex = min(inputGraph.nodes().data(),
                            key=lambda x: x[1]['loss'])[0]

            # Remove the vertex with the lowest loss
            C.remove(minVertex)

            # Update loss and gain ----------
            inputGraph.nodes()[minVertex]['age'] = 0
            inputGraph.nodes()[minVertex]['loss'] = np.inf
            newGain = 0
            for n in inputGraph.adj[minVertex]:
                if inputGraph.nodes()[n]['loss'] == np.inf:
                    newGain += 1
                    inputGraph.edges()[minVertex, n]['covered'] = False
                inputGraph.nodes()[n]['loss'] += 1
                inputGraph.nodes()[n]['gain'] += 1

            inputGraph.nodes()[minVertex]['gain'] = newGain
            # -----------------------------

            continue

        # Get a random vertex with low loss
        randVertex = BMS(C, inputGraph)

        # Get a random uncovered edge
        # Format of edge: (int:node1, int:node2, bool:'covered')
        eU, eV = random.choice(
            [(e[0], e[1]) for e in inputGraph.edges().data('covered') if e[2] != True])

        # Remove the random (low loss) vertex
        C.remove(randVertex)

        # Update loss and gain ----------
        inputGraph.nodes()[randVertex]['age'] = 0
        inputGraph.nodes()[randVertex]['loss'] = np.inf
        newGain = 0
        for n in inputGraph.adj[randVertex]:
            if inputGraph.nodes()[n]['loss'] == np.inf:
                newGain += 1
                inputGraph.edges()[randVertex, n]['covered'] = False
            inputGraph.nodes()[n]['loss'] += 1
            inputGraph.nodes()[n]['gain'] += 1

        inputGraph.nodes()[randVertex]['gain'] = newGain
        # -----------------------------

        # Choose the vertex with higher gain and break ties by age
        vg = None
        if (inputGraph.nodes()[eU]['gain'] > inputGraph.nodes()[eV]['gain']):
            vg = eU
        elif (inputGraph.nodes()[eU]['gain'] == inputGraph.nodes()[eV]['gain']):
            if (inputGraph.nodes()[eU]['age'] > inputGraph.nodes()[eV]['age']):
                vg = eU
            else:
                vg = eV
        else:
            vg = eV

        # Add the new random vertex (with high gain)
        C.append(vg)

        # Update loss and gain ----------
        inputGraph.nodes()[vg]['age'] = 0
        inputGraph.nodes()[vg]['gain'] = -np.inf
        newLoss = 0
        for n in inputGraph.adj[vg]:
            if inputGraph.nodes()[n]['loss'] == np.inf:
                newLoss += 1
                inputGraph.edges()[vg, n]['covered'] = True
            inputGraph.nodes()[n]['loss'] -= 1
            inputGraph.nodes()[n]['gain'] -= 1

        inputGraph.nodes()[vg]['loss'] = newLoss
        # -----------------------------

    return sol, trace


def ConstructVC(inputGraph):
    C = list()

    # Make so C fully covers the input graph
    for u, v in inputGraph.edges():
        # If an edge is uncovered then add the vertex with the higher degree to C
        if inputGraph.edges()[u, v]['covered'] == False:
            if (inputGraph.degree[u] > inputGraph.degree[v]):
                inputGraph.nodes()[u]['loss'] = 0
                inputGraph.nodes()[u]['gain'] = -np.inf
                C.append(u)
                for a in inputGraph.adj[u]:
                    inputGraph.edges()[u, a]['covered'] = True
            else:
                inputGraph.nodes()[v]['loss'] = 0
                inputGraph.nodes()[v]['gain'] = -np.inf
                C.append(v)
                for a in inputGraph.adj[v]:
                    inputGraph.edges()[v, a]['covered'] = True

    # Calculate the loss value for each of the vertices in C
    for u, v in inputGraph.edges():
        if (inputGraph.nodes()[u]['loss'] != np.inf and inputGraph.nodes[v]['loss'] == np.inf):
            inputGraph.nodes()[u]['loss'] += 1
        if (inputGraph.nodes()[v]['loss'] != np.inf and inputGraph.nodes[u]['loss'] == np.inf):
            inputGraph.nodes()[v]['loss'] += 1
        if (inputGraph.nodes()[v]['loss'] == np.inf and inputGraph.nodes[u]['loss'] == np.inf):
            print("!! error: constructVC found an edge not being covered !!")

    # Remove vertices that only cover edges that are already covered by other vertices
    for c in C:
        if inputGraph.nodes()[c]['loss'] == 0:
            for n in inputGraph.adj[c]:
                inputGraph.nodes()[n]['loss'] += 1
            C.remove(c)
            inputGraph.nodes()[c]['loss'] = np.inf
            inputGraph.nodes()[c]['gain'] = 0

    return C


# Best from Multiple Selections
def BMS(C, inputgraph):
    best = random.choice(C)

    # Randomly choose a vertex in C with low loss
    for i in range(50):
        r = random.choice(C)
        if inputgraph.nodes()[r]['loss'] < inputgraph.nodes()[best]['loss']:
            best = r

    return best
