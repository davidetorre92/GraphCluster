import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import igraph as ig

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

def plot_graph(G, target = None):
    vs = visual_style(G)
    if target is None:
        fig, ax = plt.subplots()
    else:
        ax = target
        fig = ax.get_figure()
        
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
