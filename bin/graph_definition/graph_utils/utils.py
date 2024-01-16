import numpy as np
import pandas as pd
import igraph as ig

def cosine_similarity(row_i, row_j):
    return np.dot(row_i, row_j) / (np.sqrt(np.dot(row_i, row_i)) * np.sqrt(np.dot(row_j, row_j)))

def euclidean_similarity(row_i, row_j):
    return np.sqrt(np.sum((row_i - row_j) ** 2, axis = -1))

def get_level_of_impairment(MMSE):
    MMSE = int(MMSE + 0.5)
    if MMSE >= 27: return 'None'
    elif MMSE < 26 and MMSE > 21: return 'Mild'
    elif MMSE < 20 and MMSE > 11: return 'Moderate'
    elif MMSE <= 10: return 'Severe'
    
def get_level_of_impairment_numeric(MMSE):
    MMSE = int(MMSE + 0.5)
    if MMSE >= 27: return 0
    elif MMSE < 26 and MMSE > 21: return 1
    elif MMSE < 20 and MMSE > 11: return 2
    elif MMSE <= 10: return 3
    else: return -1
    

def get_level_of_CDR_numeric(CDR):
    if CDR == 0: return 0
    elif CDR == 0.5: return 1
    elif CDR == 1: return 2
    elif CDR == 2: return 3
    elif CDR == 3: return 4
    else: return -1

def get_labels(labeled_df, column):
    labels = labeled_df[column].tolist()
    return labels

def get_value_key(labelled_df_path, mode = 'dementia_group'):
    df = pd.read_csv(labelled_df_path)
    if mode == 'dementia_group':
        return {0: 'Nondemented', 1: 'Demented', 2: 'Converted'}
    elif mode == 'MMSE':
        return {-1: 'NaN', 0: 'None', 1: 'Mild', 2: 'Moderate', 3:'Severe'}
    elif mode == 'CDR':
        return {-1: 'NaN', 0: 'Normal', 1: 'Very Mild Dementia', 2: 'Mild Dementia', 3:'Moderate Dementia', 4:'Severe Dementia'}
    else: raise Exception(f"Mode {mode} not implemented. Aborting...")
    

