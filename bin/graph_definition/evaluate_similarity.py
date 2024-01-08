import numpy as np
import pandas as pd

import os
from graph_utils.utils import *
import argparse
from configparser import ConfigParser

# ArgParser
parser = argparse.ArgumentParser(description = "Create similarity dataset")
parser.add_argument("--config", "-c", type = str, help = "path/to/config.ini", required=True)
args = parser.parse_args()
config_path = args.config

# Reading settings
config = ConfigParser()
config.read(config_path)

normalized_df_path = config.get('similarity', 'normalized_df_path')
similarity_df_out_path = config.get('similarity', 'similarity_df_out_path')
label_col = config.get('similarity', 'label_col')
similarity_function_option = config.get('similarity', 'similarity_function')

if similarity_function_option == 'cosine':
	similarity_function = cosine_similarity
elif similarity_function_option == 'euclidean':
	similarity_function = euclidean_similarity
else: raise Exception(f"Similarity function {similarity_function_option} not found. Aborting...")

# Settings
# normalized_df_path = '../data/make_moons.csv'
# out_path = '../data/similarity_moons.csv'
# label_col = 'cl'

normalized_df = pd.read_csv(normalized_df_path)
normalized_df.drop(label_col, axis = 1, inplace = True)

# Script
rows = []
n_rows = normalized_df.shape[0]
for i in range(n_rows):
    for j in range(i+1, n_rows):
        row_i = normalized_df.iloc[i].to_numpy()
        row_j = normalized_df.iloc[j].to_numpy()
        rows.append((i,j, similarity_function(row_i, row_j)))

similarity_df = pd.DataFrame(rows, columns=['node_i', 'node_j', 'sim'])

out_folder = os.path.dirname(similarity_df_out_path)
if os.path.exists(out_folder) is False:
    os.makedirs(out_folder)

similarity_df.to_csv(similarity_df_out_path)
print(f'Data saved in {similarity_df_out_path}, rows: {normalized_df.shape[0]}')
