import networkx as nx
import numpy as np
import scipy as sp
import scipy.linalg as sla
import matplotlib.pyplot as plt

def normalized_laplacian(A, normalize=True):
    # find degree of each nodes
    d = A.sum(axis=0)
    D = np.diag(d)
    L = D - A
    # for normalized laplacian we need 
    # L = I - D^-1/2AD^-1/2
    if normalize:
        d = d**-0.5
        D = np.diag(d)
        L = D @ L @ D

    return L

def compute_slepian_vectors(A, S, bandwith, type):
    # TODO: Check if this is true
    k = bandwith
    L = normalized_laplacian(A, normalize=True)

    # Fourier basis: the "frequencies"
    lam, U = sla.eigh(L)
    lam = np.clip(lam, 0, None) # to avoid floating point error
    W = np.eye(A.shape[0])[:,:k] # keeping the first k frequencoes
    
    # Concentration matrix based on type parameter
    if type == "mu":
        C = W.T @ U.T @ S @ U @ W
    elif type == "tzai":
        lambda_half = np.diag(np.sqrt(lam[:k]))
        C = lambda_half @ W.T @ U.T @ S @ U @ W @ lambda_half
    slepian_ev, slepian_evec = sla.eigh(C)

    return (U @ W) @ slepian_evec



def nxGraphSlepians(graph, subgraph, bandwidth, type="mu"):

    # convert the graph into adjacenecy matrix and find 
    # adjacency A and degree matrix D using slepNormalize equivalent in Python

    nodes = list(graph.nodes())
    A = nx.to_numpy_array(graph, nodelist=nodes, weight=None) # since eveyrthing else is sparse
    S = np.zeros(len(nodes))
    subgraph_n = subgraph.nodes()
    # TODO: will subgraph labels always be a number
    S[list(subgraph_n)] = 1 # Assuming that the subgraph labels are numeric, thats why this function is for networkx graphs
    S = np.diag(S)
    
    vectors = compute_slepian_vectors(A, S, bandwidth, type)
    return vectors

def plot_slepian_results(graph, subgraph, bandwidth, num_vec_show):
    
    layout = nx.spring_layout(graph, seed=1)  # for consistent positions of the nodes

    #panel per plot
    fig, axes = plt.subplots(1, num_vec_show, figsize=(4 * num_vec_show, 4))

    for val in ["mu", "tzai"]:
        vectors = nxGraphSlepians(graph, subgraph, bandwidth, val)
        if val == "mu":
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

        plt.show()


m, n = 5, 3
G_lollipop = nx.lollipop_graph(m,n)
head_sub = G_lollipop.subgraph(range(m))
tail_sub = G_lollipop.subgraph(range(m, m+n))
    

m1, n1 = 10, 5
barbell = nx.barbell_graph(m1, n1)  
left_weight = barbell.subgraph(range(0, m1))
middle = barbell.subgraph(range(m1, m1+n1))
right_weight =  barbell.subgraph(range(m1+n1, 2*(m1+n1)))

plot_slepian_results(G_lollipop, head_sub, 4, 4)
