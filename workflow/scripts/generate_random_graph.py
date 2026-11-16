import networkx as nx
import yaml 
from utils import unpack_parameters
from typing import Dict
from damply import dirs
import argparse
import matplotlib.pyplot as plt



def main(config:Dict):
    config_name, seed, num_nodes, p = unpack_parameters(config['GRAPH_INFO'])

    G = nx.gnp_random_graph(num_nodes, p,seed= seed)
    pos = nx.spring_layout(G, seed=seed) 
    # it's good to have a specified layout so the graph doesn't change with each run

    nx.draw(G,pos=pos)
    plt.savefig(dirs.RESULTS / f"{config_name}_random_graph.png")
    plt.close()








if __name__ =="__main__":
    parser = argparse.ArgumentParser(prog = "A simple program to produce a random graph")

    # we add a named argument
    parser.add_argument("-config", help = "The configuration file for the experiment.")
        
    
    args = parser.parse_args()

    with open(args.config) as config_file:
        config = yaml.safe_load(config_file)

    main(config)
