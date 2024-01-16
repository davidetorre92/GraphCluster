import os
import numpy as np
import pandas as pd
import igraph as ig

from graph_utils.utils import *
import argparse
from configparser import ConfigParser

# ArgParser
parser = argparse.ArgumentParser(description = "Create similarity graph")
parser.add_argument("--config", "-c", type = str, help = "path/to/config.ini", required=True)
args = parser.parse_args()
config_path = args.config

# Reading settings
config = ConfigParser()
config.read(config_path)

labeled_df_path = config.get('similarity', 'normalized_df_path')
similarity_df_path = config.get('similarity', 'similarity_df_out_path')
similarity_function_option = config.get('similarity', 'similarity_function')
label_col = config.get('similarity', 'label_col')
threshold = config.get('similarity', 'threshold') 
graph_path = config.get('graph options', 'graph_path')

# Script
threshold = float(threshold)
similarity_df = pd.read_csv(similarity_df_path)
labeled_df = pd.read_csv(labeled_df_path)

# Node assignation
V = labeled_df.shape[0]

# Edges definition
if similarity_function_option == 'cosine':
    edge_list = similarity_df[similarity_df['sim'] > threshold][['node_i', 'node_j']].values
elif similarity_function_option == 'euclidean':
    edge_list = similarity_df[similarity_df['sim'] < threshold][['node_i', 'node_j']].values
else: raise Exception(f"Similarity function {similarity_function_option} not found. Aborting...")

G = ig.Graph(n = V, edges = edge_list, directed = False)

# Label definition
G.vs['group'] = get_labels(labeled_df, column = label_col)
G['Label name'] = label_col
out_folder = os.path.dirname(graph_path)
if os.path.exists(out_folder) is False:
    print(f"Creating the folder {out_folder}")
    os.makedirs(out_folder)

G.write_graphml(graph_path)
print(f"Graph saved in {graph_path}")
print("")
print(G.summary())
