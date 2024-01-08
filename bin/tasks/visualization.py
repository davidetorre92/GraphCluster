import numpy as np
import pandas as pd

import os
import igraph as ig

import matplotlib as mpl
import matplotlib.pyplot as plt
from graph_definition.graph_utils.utils import *

# ArgParser
parser = argparse.ArgumentParser(description = "Create similarity graph")
parser.add_argument("--config", "-c", type = str, help = "path/to/config.ini")
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

# Settings
group_order = [0, 1]
plot_size = 2

if os.path.exists(os.path.dirname(eda_path)) is False:
    raise Warning(f"{eda_path} does not exists, creating now...")
    os.makedirs(os.path.dirname(eda_path))
    
# Script
## 1. Read graph
G = ig.Graph.Read_GraphML(graph_path)

# EDA
## Degree distribution
print("Plotting degree distribution...")
fig, ax = plot_degree_distribution(G)
img_path = os.path.join(eda_path, 'degree_distribution.pdf')
fig.savefig(img_path)
print(f"Degree distribution saved in {img_path}")
print()

## Graph
print("Plotting the graph...")
fig, ax = plot_graph(G)
fig.tight_layout()
img_path = os.path.join(eda_path, f'graph.pdf')
fig.savefig(img_path)
print(f"Graph visualization saved in {img_path}")
print()
## Correlations
print("Plotting correlation...")
rows = []

if 'group_order' in globals():
    unique_labels = group_order
else:
    unique_labels = np.unique(G.vs['group'])
for v_i in G.vs():
    neighbors_of_v_i = v_i.neighbors()
    neighbour_data = {label: 0 for label in unique_labels}
    for v_j in neighbors_of_v_i:
        neighbour_data[v_j['group']] += 1
    degree_v_i = v_i.degree()
    if degree_v_i != 0: row = [v_i.index, v_i['group'], degree_v_i] + [neighbour_data[key] / degree_v_i for key in unique_labels]
    else: row = [v_i.index, v_i['group'], degree_v_i] + [0 for _ in unique_labels]
    rows.append(row)

fraction_cols = [f'fraction_group_{label}' for label in unique_labels]
columns = ['node_id', 'node_group', 'node_degree'] + fraction_cols
df_corr = pd.DataFrame(rows, columns=columns)

n_labels = len(unique_labels)

fig, axs = plt.subplots(n_labels, n_labels, figsize=(n_labels * plot_size,n_labels * plot_size))

for irow, label_i in enumerate(unique_labels):
    df_group = df_corr[df_corr['node_group'] == label_i]
    for icol, label_j in enumerate(unique_labels):
        # irow = group_i - min(unique_labels)
        # icol = group_j - min(unique_labels)
        data = df_group.loc[:,f'fraction_group_{label_j}']
        bins = np.linspace(0,1,20)
        counts, edges = np.histogram(data, bins)
        frq = counts / np.sum(counts)
        axs[irow][icol].bar(edges[:-1], frq, width = np.diff(edges), align = 'center')
        axs[irow][icol].set_title(f'{label_i} vs {label_j}', size = 8)
        axs[irow][icol].set_xlabel('Fraction', size = 4)
        axs[irow][icol].set_ylabel('Proportion', size = 4)
        axs[irow][icol].set_xlim((0,1))
        axs[irow][icol].set_ylim((0,1))
        axs[irow][icol].grid('both')
fig.tight_layout()

img_path = os.path.join(eda_path, f"correlation_group_all_{G['Label name']}.pdf")
fig.savefig(img_path)
print(f"Neighbour correlation saved in {img_path}")


