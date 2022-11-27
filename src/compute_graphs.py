import sys, os
sys.path.append(os.getcwd())

from src.run_mvc import main
import argparse

# run all files in experiments

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-graph_dir', default='data/', help='graph directory')
    parser.add_argument('-alg', default='BnB',help='algorithm option option')
    parser.add_argument('-time', default=240, type=float, help='time limit option')
    parser.add_argument('-seed', default=0, type=float, help='seed option')
    args = parser.parse_args()

    set_graphs = []
    data_dir = args.graph_dir
    for file in os.listdir(data_dir):
        # print(args.graph_dir+file)
        set_graphs.append(args.graph_dir+file)
    
    algorithm = args.alg
    cutoff_limit = int(args.time)
    random_seed = int(args.seed)
    
    for file_name in set_graphs:
        main(file_name, algorithm, cutoff_limit, random_seed)

