import numpy as np
import pandas as pd

import os
from graph_utils.utils import *

# Settings
normalized_df_path = '/home/davide/ai/Projects/AD/AD preprocess/oasis_normalized.csv'
similarity_function = cosine_similarity
out_path = '/home/davide/ai/Projects/AD/similarity.csv'

normalized_df = pd.read_csv(normalized_df_path)
# Script
rows = []
n_rows = normalized_df.shape[0]
for i in range(n_rows):
    for j in range(i+1, n_rows):
        row_i = normalized_df.iloc[i].to_numpy()
        row_j = normalized_df.iloc[j].to_numpy()
        rows.append((i,j, similarity_function(row_i, row_j)))

similarity_df = pd.DataFrame(rows, columns=['node_i', 'node_j', 'sim'])

out_folder = os.path.dirname(out_path)
if os.path.exists(out_folder) is False:
    os.makedirs(out_folder)

similarity_df.to_csv(out_path)
print(f'Data saved in {out_path}, patients: {normalized_df.shape[0]}')
