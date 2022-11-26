import sys, os
sys.path.append(os.getcwd())

import networkx as nx
import argparse
from src.branch import branch_and_bound
from src.approx import approxVC


# This file contians logic to run all algorithms (BnB, Approx, LS1, and LS2) to find a minimum vertex cover on a given graph

"""
Inputs:
    -inst:  file location of the graph 
    -alg:   the algorithm to be used (BnB, Approx, LS1, LS2)
    -time:  the cutoff time limit
    -seed:  the random seed for randomized algorithms
To call this in command line, type 'python src/run_mvc.py -inst <graph file name> -alg [BnB|Approx|LS1|LS2] -time <cutoff in seconds> -seed <random seed>
"""
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-inst', default='data/dummy1.graph', help='filename option')
    parser.add_argument('-alg', default='BnB',help='algorithm option option')
    parser.add_argument('-time', default=20, type=float, help='time limit option')
    parser.add_argument('-seed', default=0, type=float, help='seed option')
    args = parser.parse_args()

    file_name = args.inst
    algorithm = args.alg
    cutoff_limit = int(args.time)
    random_seed = int(args.seed)

    graphfile = open(file_name,'r')
    lines = graphfile.readlines()
    Vnum,Enum,n = lines[0].split()
    graph = nx.Graph()
    for i, line in enumerate(lines):
        if i != 0:
            vals = line.split()
            for j in vals:
                graph.add_edge(int(i), int(j))

    output_dir = "solutions/" + file_name.split("/")[-1] + "_" + algorithm + "_" + str(cutoff_limit)

    if (args.alg == 'BnB'):
        sol_dir = output_dir+".sol"
        trace_dir = output_dir+".trace"
        sol, trace = branch_and_bound(graph, cutoff_limit)
        sol1 = open(sol_dir,'w')
        sol1.write(str(len(sol)))
        sol1.write("\n")
        sol1.write(','.join([str(s) for s in sol]))
        sol1.close()
        trace1 = open(trace_dir,'w')
        for line in trace:
            trace1.write(line)
            trace1.write("\n")
        trace1.close()

    elif (args.alg == 'Approx'):
        output_dir += ("_" + str(random_seed))
        sol_dir = output_dir + ".sol"
        trace_dir = output_dir + ".trace"
        sol, trace = approxVC(graph, cutoff_limit, random_seed)
        #print(trace)
        sol1 = open(sol_dir, 'w')
        sol1.write(str(len(sol)))
        sol1.write("\n")
        sol1.write(','.join([str(s) for s in sol]))
        sol1.close()
        trace1 = open(trace_dir, 'w')
        for time, vertices in trace:
            time = round(time, 2)
            trace1.write(str(time) + ", " + str(vertices))
            trace1.write("\n")
        trace1.close()
    
    elif (args.alg == 'LS1'):
        pass
    
    elif (args.alg == 'LS2'):
        pass