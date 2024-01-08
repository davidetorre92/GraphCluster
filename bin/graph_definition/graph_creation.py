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
edge_list = similarity_df[similarity_df['sim'] > threshold][['node_i', 'node_j']].values
G = ig.Graph(n = V, edges = edge_list, directed = False)

# Label definition
G.vs['group'] = get_labels(labeled_df, column = label_col)
G['Label name'] = label_col
G.write_graphml(graph_path)

print(G.summary())
