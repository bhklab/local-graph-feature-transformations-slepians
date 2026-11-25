import networkx as nx
import numpy as np
import scipy as sp
import scipy.linalg as sla
import matplotlib.pyplot as plt
from damply import dirs

from produce_eigenvec_plots import normalized_laplacian
from produce_eigenvec_plots import nxGFT

def _fix_sign(M): 
    """
    This 'fixes' the sign of a set of vectors [u], so that u vs -u does
    not give different signs when used for plotting. They are the same eigenvector
    so they should be plotted in the same way, disregarding the sign that sla.eigh picks
    """
    M = np.array(M, dtype=float, copy=True)
    idx = np.argmax(np.abs(M), axis=0)                 
    signs = np.sign(M[idx, np.arange(M.shape[1])])     
    signs[signs == 0] = 1                              
    return M * signs  

def compute_slepian_vectors(A, S, bandwith, type):
    """
    Using adjacency matrix A, and the selection matrix S compute mu and xi slepian vectors
    Bandwidth parameter gives frequency restriction
    Selection matrix S, gives the subgraph that we are restricted to
    Type parameter is either ("mu", "xi") 
    """
    # TODO: Confirm how k comes as an input, is it just a number
    k = bandwith
    # Build laplacian matrix
    L = normalized_laplacian(A, normalize=True)

    # Compute the fourier basis using eigendecomposition of the laplacian
    # Cols of U are the fourier basis and lam are the frequencies (asc order)
    lam, U = sla.eigh(L)
    lam = np.clip(lam, 0, None) # to avoid floating point error when we do sqrt later
    W = np.eye(A.shape[0])[:,:k] # Identity matrix that keeps only the first k frequncies, will be used with U

    # Concentration matrix based on type parameter
    if type == "mu":
        C = W.T @ U.T @ S @ U @ W
    elif type == "xi":
        lambda_half = np.diag(np.sqrt(lam[:k]))
        C = lambda_half @ W.T @ U.T @ S @ U @ W @ lambda_half
    # Compute eigendecomposition of new matrix
    # Eigenvectors solve the optimization problem for each vector type
    # mu: lowest eigenvalue -> lowest concentration on the subgraph
    # xi: lowest eigenvalue -> smoothest signal on the subgraph
    slepian_ev, slepian_evec = sla.eigh(C)

    # Multiply with U @ W to move back into the node domain
    # So each slepian vector is defined per node
    return (U @ W) @ slepian_evec


def nxGraphSlepians(graph, subgraph, bandwidth, type="mu"):
    """
    Wrapper function that finds slepian vectors for NetworkX graphs specifically
    """

    # Create adjacency and selection matrices
    nodes = list(graph.nodes())
    A = nx.to_numpy_array(graph, nodelist=nodes, weight=None) # since eveyrthing else is sparse
    S = np.zeros(len(nodes))
    subgraph_n = subgraph.nodes()
    # TODO: will subgraph labels always be a number
    S[list(subgraph_n)] = 1 # Assuming that the subgraph labels are numeric, thats why this function is for networkx graphs
    S = np.diag(S)
    
    # Call main compute_slepian_vectors to get slepian vectors
    vectors = compute_slepian_vectors(A, S, bandwidth, type)
    return vectors

def plot_slepian_results(graph, subgraph, bandwidth, num_vec_show):
    """
    Draws the vectors as node colors on the graph

    num_vec_show: Number of vectors from slepian vectors to show
    """

    # Fix node poistions for consistency across all node panels
    layout = nx.spring_layout(graph, seed=1)  # for consistent positions of the nodes

    # One panel per plot
    fig, axes = plt.subplots(1, num_vec_show, figsize=(4 * num_vec_show, 4))

    # Compute a plot for each vector type
    for val in ["mu", "xi"]:
        vectors = nxGraphSlepians(graph, subgraph, bandwidth, val)
        if val == "mu":
            # Reverse order, because highest eigenvectors mean most concentration
            columns = list(range(bandwidth))[::-1][:num_vec_show]
        else:
            columns = list(range(bandwidth))[:num_vec_show]
        for axis, col_idx in zip(axes, columns):
            vectors = nxGraphSlepians(graph, subgraph, bandwidth, val)
            
            v = vectors[:,col_idx]

            if v[np.argmax(np.abs(v))] < 0:             
                v = -v
            limit = np.abs(v).max()
            nx.draw(graph, layout, ax=axis, node_color=v, cmap="coolwarm", vmin=-limit, vmax=limit)
            axis.set_title(f"type: {val}, slepian vector {col_idx + 1}")

        plt.savefig(dirs.RESULTS / f"{val}_slepians.png")
        plt.close()

def plot_coeff(signal, graph, name, subgraph, bandwidth):

    mu = nxGraphSlepians(graph, subgraph, bandwidth, type="mu")
    xi = nxGraphSlepians(graph, subgraph, bandwidth, type="xi")
    mu = mu[:, ::-1]  
    lam, U = nxGFT(graph)
    signal = np.asarray(signal,dtype=float)
    n = U.shape[1]

    # dot/inner products
    U, mu, xi = _fix_sign(U), _fix_sign(mu), _fix_sign(xi)

    u_c = U.T @ signal
    mu_c = mu.T @ signal
    xi_c = xi.T @ signal

    colors = {"u":"tab:red", "xi":"tab:blue","mu":"tab:orange"}
    fig,ax = plt.subplots(figsize=(8,4.5), layout="constrained")

    width = 0.30
    x = np.arange(n)
    ax.bar(x[:bandwidth] - width, u_c[:bandwidth], width, color="tab:red", label="eigenvector")
    ax.bar(x[:bandwidth] , mu_c, width, color="tab:orange", label="mu slepians")
    ax.bar(x[:bandwidth] + width, xi_c, width, color="tab:blue", label="xi slepian")
    ax.bar(x[bandwidth:] , u_c[bandwidth:], width, color="tab:red")

    ax.set_xlabel("index j")
    ax.set_ylabel("⟨signal, vector⟩")
    ax.set_title(f"Signal coefficients on {name} graph (bandwidth = {bandwidth})")
    ax.legend()

    plt.savefig(dirs.RESULTS / f"signal_coefficients.png")
    plt.close()

m, n = 5, 3
G_lollipop = nx.lollipop_graph(m,n)
head_sub = G_lollipop.subgraph(range(m))
tail_sub = G_lollipop.subgraph(range(m, m+n))
    

m1, n1 = 10, 5
barbell = nx.barbell_graph(m1, n1)  
left_weight = barbell.subgraph(range(0, m1))
middle = barbell.subgraph(range(m1, m1+n1))
right_weight =  barbell.subgraph(range(m1+n1, 2*(m1+n1)))

# plot_slepian_results(G_lollipop, head_sub, 4, 4)
sig = np.array([0, 0, 0, 0, 0, 1, 1, 1], dtype=float)
plot_coeff(sig, G_lollipop, "lollipop", head_sub, 4)