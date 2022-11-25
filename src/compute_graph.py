#!/usr/bin/python
# CSE6140 HW2
# This is an example of how your experiments should look like.
# Feel free to use and modify the code below, or write your own experimental code, as long as it produces the desired output.
import time
import sys
import os
import matplotlib.pyplot as plt
import operator
from tqdm import tqdm

class Graph:
    def __init__(self, edges, endpoints, max_index) -> None:
        self.edges = edges
        self.endpoints = endpoints
        self.edge_dictionary = {}

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

        # counter = len(G.mst_edges)-1
        # while counter >= 0:
        #     if weight < G.edges
        # for idx, (node1, node2) in enumerate(G.endpoints):
        #     if ((u==node1 and v==node2) or (u==node2 and v==node1)) and idx in G.mst_edges:
        #         print("here")
        #         if weight < G.edges[idx]:
        #             G.total_weight -= G.edges[idx]
        #             G.total_weight += weight
        #             G.edges.append(weight)
        #             G.mst_edges.remove(idx)
        #             G.mst_edges.add(len(G.endpoints))
        #             G.endpoints.append((u, v))
        return G.total_weight


if __name__ == '__main__':
    # run all files in experiments
    set_graphs = set()
    
    num_args = len(sys.argv)

    if num_args != 2:
        print("error: not enough input arguments")
        exit(1)

    data_dir = sys.argv[1]
    for file in os.listdir(data_dir):
        split_f = file.split('.')
        set_graphs.add(split_f[0])
    
    edge_size = []
    mst_time = []
    recompute_time = []
    for file_name in set_graphs:
        print(file_name)
        runexp = RunExperiments()
        graph_file = data_dir+file_name+'.gr'
        change_file = data_dir+file_name+'.extra'

        # Construct graph
        G = runexp.parse_edges(graph_file)
        edge_size.append(len(G.edges))

        start_MST = time.time()  # time in seconds
        # call MST function to return total weight of MST
        MSTweight = runexp.computeMST(G)
        total_time = (time.time() - start_MST) * \
            1000  # to convert to milliseconds
        mst_time.append(total_time)

        total_re = 0
        # Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in tqdm(changes):
                # parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u, v, weight = edge_data[0], edge_data[1], edge_data[2]

                # call recomputeMST function
                start_recompute = time.time()
                new_weight = runexp.recomputeMST(u, v, weight, G)
                # to convert to milliseconds
                total_recompute = (time.time() - start_recompute) * 1000
                total_re += total_recompute
        
        recompute_time.append(total_re)
    
    plt.scatter(edge_size, mst_time)
    plt.ylabel('Dynamic MST Calculation Time')
    plt.xlabel('Number of Edges')
    plt.title('Dynamic MST Computation Time vs Number of Edges')
    plt.savefig(f'results/dynamic_mst.png')

    plt.clf()
    plt.scatter(edge_size, recompute_time)
    plt.ylabel('Static MST Recompute Time')
    plt.xlabel('Number of Edges')
    plt.title('Static MST Recompute Time vs Number of Edges')
    plt.savefig(f'results/static_mst.png')


