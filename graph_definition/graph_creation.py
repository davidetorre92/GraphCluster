import numpy as np
import pandas as pd

import igraph as ig
from graph_utils.utils import *

# Settings
similarity_df_path = '/home/davide/ai/Projects/AD/data/similarity_1.csv'
threshold = 0.85
labeled_df_path = '/home/davide/ai/Projects/AD/data/oasis_labeled.csv'
graph_path = '/home/davide/ai/Projects/AD/data/sim.graphml'
label_col = 'Group'

# Script
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
