#!/usr/bin/python
# CSE6140 HW2
# This is an example of how your experiments should look like.
# Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
import time
import sys
import operator

class Graph:
    def __init__(self, edges, endpoints, max_index) -> None:
        self.edges = edges
        self.endpoints = endpoints
        self.edge_dictionary = {}
        for idx, (u,v) in enumerate(endpoints):
            if u in self.edge_dictionary:
                self.edge_dictionary[u].append((v, idx))
            else:
                self.edge_dictionary[u] = [(v, idx)]
            if v in self.edge_dictionary:
                self.edge_dictionary[v].append((u, idx))
            else:
                self.edge_dictionary[v] = [(u, idx)]

        self.mst_edges = None
        self.sorted_edges = None
        self.total_weight = None

        self.n = max_index
        self.cycle = [i for i in range(self.n)]
    
    def find(self, i):
        if i != self.cycle[i]:
            self.cycle[i] = self.find(self.cycle[i])
        return self.cycle[i]

    def union(self, i, j):
        pi, pj = self.find(i), self.find(j)
        if pi != pj:
            self.cycle[pi] = pj

    def connected(self, i, j):
        return self.find(i) == self.find(j)


class RunExperiments:
    def parse_edges(self, filename):
        # Write this function to parse edges from graph file to create your graph object
        with open(filename, 'r') as file:
            num_vertices_edges = file.readline()
            num_vertices_edges = list(map(lambda x: int(x), num_vertices_edges.split()))
            edges = []
            vertices = []
            max_index = -1
            for _ in range(num_vertices_edges[1]):
                line = file.readline()
                sp_edge = list(map(lambda x: int(x), line.split()))
                edges.append(sp_edge[2])
                if sp_edge[0] < sp_edge[1]:
                    vertices.append((sp_edge[0], sp_edge[1]))
                else:
                    vertices.append((sp_edge[1], sp_edge[0]))
                max_index = max(sp_edge[0], max_index)
                max_index = max(sp_edge[1], max_index)
            return Graph(edges, vertices, max_index+1)


    # Calc partial solution and prune on lower bound
    def computeMST(self, G):
        # Write this function to compute total weight of MST
        mst_edges = set()
        sorted_pairs = sorted(enumerate(G.edges), key=operator.itemgetter(1), reverse=True)

        total_weight = 0
        for index, weight in sorted_pairs:
            if not G.connected(G.endpoints[index][0], G.endpoints[index][1]):
                mst_edges.add(index)
                G.union(G.endpoints[index][0], G.endpoints[index][1])
                total_weight += weight
        
        for edge_idx in mst_edges:
            (u,v) = G.endpoints[edge_idx]
            if u in G.edge_dictionary:
                G.edge_dictionary[u].append((v, edge_idx))
            else:
                G.edge_dictionary[u] = [(v, edge_idx)]
            if v in G.edge_dictionary:
                G.edge_dictionary[v].append((u, edge_idx))
            else:
                G.edge_dictionary[v] = [(u, edge_idx)]
        
        G.mst_edges = mst_edges
        G.sorted_pairs = sorted_pairs
        G.total_weight = total_weight
        return total_weight


    def recomputeMST(self, u, v, weight, G):
        # Write this function to recompute total weight of MST with the newly added edge
        # check which edge from MST between nodes u and v is used, substitute if weight is lower

        # use dfs to find path from u to v, keep track of edges in path
        # if weight of any edge in path is greater than new edge, remove and add new edge
        predecessor = {u: (u, None)}
        visited = set()
        stack = [u]
        current_node = None
        # print(G.mst_edges)


        while current_node != v and len(stack) > 0:
            current_node = stack.pop()
            visited.add(current_node)
            successors = G.edge_dictionary[current_node]
            for node in successors:
                if node[0] not in visited:
                    predecessor[node[0]] = current_node, node[1]
                    stack.append(node[0])

        # backtrack through predecessors
        largest_weight_cycle = None
        largest_weight_idx = None
        current_node = v
        while predecessor[current_node][0] != current_node:
            if largest_weight_cycle is None or G.edges[predecessor[current_node][1]] > largest_weight_cycle:
                largest_weight_cycle = G.edges[predecessor[current_node][1]]
                largest_weight_idx = predecessor[current_node][1]
            current_node = predecessor[current_node][0]
        
        if weight < largest_weight_cycle:
            G.mst_edges.remove(largest_weight_idx)
            (old_u, old_v) = G.endpoints[largest_weight_idx]
            for i in range(len(G.edge_dictionary[old_u])):
                if G.edge_dictionary[old_u][i][1] == largest_weight_idx:
                    G.edge_dictionary[old_u].pop(i)
                    break
            for i in range(len(G.edge_dictionary[old_v])):
                if G.edge_dictionary[old_v][i][1] == largest_weight_idx:
                    G.edge_dictionary[old_v].pop(i)
                    break

            G.total_weight -= largest_weight_cycle
            G.total_weight += weight
            G.edges.append(weight)
            edge_idx = len(G.endpoints)
            G.mst_edges.add(edge_idx)
            G.endpoints.append((u, v))
            G.edge_dictionary[u].append((v, edge_idx))
            G.edge_dictionary[v].append((u, edge_idx))

        return G.total_weight


    def main(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        # Construct graph
        G = self.parse_edges(graph_file)

        start_MST = time.time()  # time in seconds
        # call MST function to return total weight of MST
        MSTweight = self.computeMST(G)
        total_time = (time.time() - start_MST) * \
            1000  # to convert to milliseconds

        # Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time))

        # Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                # parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                # call recomputeMST function
                start_recompute = time.time()
                new_weight = self.recomputeMST(u, v, weight, G)
                # to convert to milliseconds
                total_recompute = (time.time() - start_recompute) * 1000

                # write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute))

    def running_time(self):

        num_args = len(sys.argv)

        if num_args < 4:
            print("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        # Construct graph
        G = self.parse_edges(graph_file)

        start_MST = time.time()  # time in seconds
        # call MST function to return total weight of MST
        MSTweight = self.computeMST(G)
        total_time = (time.time() - start_MST) * \
            1000  # to convert to milliseconds

        # Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time))

        # Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                # parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                # call recomputeMST function
                start_recompute = time.time()
                new_weight = self.recomputeMST(u, v, weight, G)
                # to convert to milliseconds
                total_recompute = (time.time() - start_recompute) * 1000

                # write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute))


if __name__ == '__main__':
    # run the experiments
    runexp = RunExperiments()
    runexp.main()
