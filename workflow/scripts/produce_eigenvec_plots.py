import networkx as nx
import numpy as np
import scipy as sp
import scipy.linalg as sla
import matplotlib.pyplot as plt
from damply import dirs

def normalized_laplacian(A, normalize=True):
    """
    Builds the graph laplacian from an adjacency matrix A
    """
    # Find degree of each node
    d = A.sum(axis=0)
    # Create the degree matrix
    D = np.diag(d)
    L = D - A
    # To produce the normalized laplacian we need L = I - D^-1/2AD^-1/2
    if normalize:
        d = d**-0.5
        D = np.diag(d)
        L = D @ L @ D

    return L

def compute_eigenvectors(A):
    """
    Using adjacency matrix A compute eigenvectors vectors
    """    
    # Build laplacian matrix
    L = normalized_laplacian(A, normalize=True)

    # Compute the graph fourier basis using eigendecomposition of the laplacian
    # Cols of U are the fourier basis and lam are the frequencies (asc order)
    lam, U = sla.eigh(L)
    lam = np.clip(lam, 0, None) # to avoid floating point error when we do sqrt later

    return lam, U

def nxGFT(graph):
    """
    Wrapper function that finds eigenvectors for NetworkX graphs specifically
    """
    # Create adjacency and selection matrices
    nodes = list(graph.nodes())
    A = nx.to_numpy_array(graph, nodelist=nodes, weight=None) # since eveyrthing else is sparse
    
    # Call main compute_slepian_vectors to get slepian vectors
    eigenvalues, eigenvectors = compute_eigenvectors(A)
    return eigenvalues, eigenvectors

def plot_graph(graph,name):
    """
    Draws graph
    """

    # Fix node poistions for consistency across all node panels
    layout = nx.spring_layout(graph, seed=1)  # for consistent positions of the nodes
    fig, ax = plt.subplots(figsize=(8,8), layout="constrained")
    nx.draw_networkx_edges(graph, layout, ax=ax, edge_color="lightgrey")
    nx.draw_networkx_nodes(graph, layout, ax=ax, node_color="orange", node_size=100)

    ax.set_title(f"{name} graph ")


    plt.savefig(dirs.RESULTS / f"{name}_graph_plot.png")
    plt.close(fig)

def plot_signal(graph, signal, name):
    signal = np.asarray(signal, dtype=float)
    # Fix node poistions for consistency across all node panels
    layout = nx.spring_layout(graph, seed=1)  # for consistent positions of the nodes
    fig, ax = plt.subplots(figsize=(8,8), layout="constrained")
    nx.draw_networkx_edges(graph, layout, ax=ax, edge_color="lightgrey")
    nodes_color = nx.draw_networkx_nodes(graph, layout, ax=ax, node_color=signal, cmap="coolwarm", node_size=60)
    
    ax.set_title(f"Signal on {name} graph ")

    fig.colorbar(nodes_color, ax=ax, shrink=0.5, label="signal value")
    plt.savefig(dirs.RESULTS / f"signal_on_{name}_graph.png")
    plt.close(fig)

def plot_random_signals(graph, name, num_sigs=1):
    rng = np.random.default_rng(seed=0)      
    for _ in range(num_sigs):
        n = graph.number_of_nodes()
        signal = rng.normal(0, 1, size=n) 
        plot_signal(graph, signal, name)
    
    
    
def plot_GFT_results(graph, filename):
    """
    Draws the eigenvectors as node colors on the graph
    """

    edges = list(graph.edges())
    nodes = list(graph.nodes())
    indices = {}
    for i in range(len(nodes)):
        indices[nodes[i]] = i

    lam, U = nxGFT(graph)
    n = len(nodes)

   
    # Fix node poistions for consistency across all node panels
    layout = nx.spring_layout(graph, seed=1)  # for consistent positions of the nodes

    # establish the eigenvector with the largest absolute value
    max_abs = np.abs(U).max()
    vlim = max_abs

    # Square plot
    ncols = int(np.ceil(np.sqrt(n)))
    nrows = int(np.ceil(n / ncols))
    # One panel per plot
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4*nrows), squeeze=False, layout="constrained")

    # Compute a plot for each vector type
    axes_flat = axes.ravel()
    for i in range(n):
        ax = axes_flat[i]
        v = U[:,i]
        # sla.eigh can give +ve or -ve version of the eigenvector, this standardizes it
        if v[np.argmax(np.abs(v))] < 0:
            v = -v
        nx.draw_networkx_edges(graph, layout, ax=ax, edge_color="lightgrey")
        nodes_color = nx.draw_networkx_nodes(graph, layout, ax=ax, node_color=v, cmap="coolwarm", vmin=-vlim, vmax=vlim, node_size=60)
        ax.set_title(f"Eigenvector u_{i+1} with eigenvalue: {lam[i]:.2f}")


    fig.colorbar(nodes_color, ax=axes.ravel().tolist(), shrink=0.5, label="eigenvector value")
    plt.savefig(dirs.RESULTS / filename)
    plt.close(fig)

m, n = 5, 3
G_lollipop = nx.lollipop_graph(m,n)
plot_GFT_results(G_lollipop, "lollipop_eigenvectors")
plot_graph(G_lollipop, "Lollipop")
plot_random_signals(G_lollipop,"Lollipop")
