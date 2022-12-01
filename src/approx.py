# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import collections
import random
import sys
import time


def approxVC(inputGraph, cutoffTime, randomSeed):
    startTime = time.time()
    mainEdgeSet = set(inputGraph.edges())
    for u, v in inputGraph.edges():
        mainEdgeSet.add((v, u))

    minVertices = sys.maxsize
    solutionTrace = []
    timetoBetterSoln = None
    finalVertexCover = []
    n = len(inputGraph)
    while time.time() - startTime < cutoffTime:
        edgeSet = mainEdgeSet.copy()
        vertexCover = set()

        while len(edgeSet) > 0 and time.time() - startTime < cutoffTime:

            if len(vertexCover) > minVertices:
                break

            lst = list(edgeSet)
            random.shuffle(lst)
            u, v = lst.pop()
            edgeSet = set(lst)

            if time.time() - startTime >= cutoffTime:
                break
            edgeSet.remove((v, u))
            vertexCover.add(u)
            vertexCover.add(v)

            # remove all edges adjacent to nodes u, and v
            for neighbor in inputGraph[u]:
                if (u, neighbor) in edgeSet:
                    edgeSet.remove((u, neighbor))
                if (neighbor, u) in edgeSet:
                    edgeSet.remove((neighbor, u))

            for neighbor in inputGraph[v]:
                if (v, neighbor) in edgeSet:
                    edgeSet.remove((v, neighbor))
                if (neighbor, v) in edgeSet:
                    edgeSet.remove((neighbor, v))

        # check if we have found a better solution.
        # if we have, then update our solution trace, time to better solution, and final vertex cover
        if len(vertexCover) < minVertices and time.time() - startTime < cutoffTime:
            minVertices = len(vertexCover)
            finalVertexCover = vertexCover
            timetoBetterSoln = (time.time() - startTime)
            solutionTrace.append((timetoBetterSoln, minVertices))

    return finalVertexCover, solutionTrace






