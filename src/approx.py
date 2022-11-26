# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import collections
import random
import sys
import time


class RunExperiments:

    def computeAdjList(self, graphFile):
        path = "DATA/" + graphFile
        adjList = collections.defaultdict(list)
        edgeSet = set()
        with open(path) as file:
            inputList = file.readlines()
            index = 0

            for index, line in enumerate(inputList):
                if index == 0:
                    vertices, edges, _ = line.split(" ")
                else:
                    neighbors = line.split(" ")
                    for neighbor in neighbors:
                        if neighbor != "\n":
                            adjList[index].append(int(neighbor))
                            edgeSet.add((index, int(neighbor)))


        return adjList, edgeSet

    def approxVC(self, inputGraph, mainEdgeSet, startTime, cutoffTime):
        minVertices = sys.maxsize
        solutionTrace = []
        timetoBetterSoln = None
        finalVertexCover = []
        n = len(inputGraph)
        while time.time() - startTime < cutoffTime:
            edgeSet = mainEdgeSet.copy()
            vertexCover = set()

            while len(edgeSet) > 0 and time.time() - startTime < cutoffTime:
                """
                while time.time() - startTime < cutoffTime:
                    u = random.randint(0, n)
                    v = random.randint(0, n)

                    if (u, v) in edgeSet:
                        edgeSet.remove((u, v))
                        break
                """



                if len(vertexCover) > minVertices:
                    break




                lst = list(edgeSet)
                random.shuffle(lst)
                u, v = lst.pop()
                edgeSet = set(lst)







                #u, v = edgeSet.pop()


                if time.time() - startTime >= cutoffTime:
                    break
                edgeSet.remove((v, u))
                vertexCover.add(u)
                vertexCover.add(v)

                #remove all edges adjacent to nodes u, and v
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

        return solutionTrace, finalVertexCover, timetoBetterSoln

    def main(self):
        num_args = len(sys.argv)

        if num_args < 3:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        cutoffTime = int(sys.argv[2])

        # compute adjacency list from input file
        adjList, edgeSet = self.computeAdjList(graph_file)
        startTime = time.time()

        # compute minimum vertex cover using given adjacency list
        solutionTrace, finalVertexCover, timeToBetterSoln = self.approxVC(adjList, edgeSet, startTime, cutoffTime)
        print(solutionTrace)
        #print(finalVertexCover)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runexp = RunExperiments()
    runexp.main()



