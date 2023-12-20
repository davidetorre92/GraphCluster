import numpy as np
import pandas as pd
import igraph as ig
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def cosine_similarity(row_i, row_j):
    return np.dot(row_i, row_j) / (np.sqrt(np.dot(row_i, row_i)) * np.sqrt(np.dot(row_j, row_j)))

def euclidean_similarity(row_i, row_j):
    delta = row_i - row_j
    return np.sqrt(np.dot(delta, delta))

# Visualization function
def visual_style(G, layout=None):
    # set layout    
    if layout is None:
        layout = G.layout_fruchterman_reingold(niter=1000)


    palette = {
        -1: '#888888', 
        0: '#1f77b4',
        1: '#ff7f0e',
        2: '#2ca02c',
        3: '#d62728',
        4: '#9467bd',
    }
    try:
        G.vs[0]['group']
    except:
        raise Exception("Label names not available. Aborting...")
    
    color_look_up_table = {key:value for value, key in enumerate(np.unique(G.vs['group']))}

    # set visual style
    visual_style = {}
    ## change label size
    visual_style['vertex_size'] = 0.2
    ## change color
    visual_style['vertex_color'] = [palette[color_look_up_table[v['group']]] for v in G.vs()]
    ## change the width of the verteces
    visual_style['vertex_frame_width'] = 0.2


    ## set edge color to be gray. The higher the weight of the lower the transparancy
    visual_style['edge_color'] = [(0.5, 0.5, 0.5, 1) for e in G.es()]
    ## change edge width
    visual_style['edge_width'] = 0.1

    ## set the layout into the dictionary
    visual_style['layout'] = layout

    return visual_style

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
    
def plot_graph(G, target = None):
    vs = visual_style(G)
    if target is None:
        fig, ax = plt.subplots()
    else:
        ax = target
        fig = ax.get_gca()
        
    ig.plot(G, target = ax, **vs)

    # Setting the handles
    color_label = set()
    labels = G.vs['group']
    colors = vs['vertex_color']
    for color, label in zip(colors, labels):
        color_label.add((color, label))

    handles = [mpatches.Circle((0.5, 0.5), 0.5, facecolor = color, label = label) for color, label in color_label]
    handles = handles + [mpatches.Circle((0.0, 0.0), 0.0, color = 'white')]
    ax.set_title(f'Graph visualization')
    ax.legend(handles = handles, bbox_to_anchor=(1.0, 0.05))
    return fig, ax

def plot_degree_distribution(G, target = None):
    if target is None:
        fig, ax = plt.subplots()
    else:
        ax = target
        fig = ax.get_gca()
        
    degree = G.degree()
    bins = np.arange(0, np.max(degree) + 1, step=1)
    counts, bins = np.histogram(degree, bins = bins)
    ax.scatter(bins[:-1], counts)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.grid(which='both')
    ax.set_title('Degree distribution (all nodes)')
    return fig, ax