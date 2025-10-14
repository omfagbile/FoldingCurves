import numpy as np
import matplotlib.pyplot as plt

class GraphDirectedIFS:
    def __init__(self, d, n, edges):
        """
        Implements a GraphDirectedIFS in R^d.
        
        Parameters:
        d (int): Dimension of R^d.
        n (int): Number of vertices.
        edges (dict): A dictionary mapping each vertex to a list of tuples (target_vertex, (A, b)),
                      where A is a linear transformation matrix and b is a translation vector.
                      For example:
                      edges = {
                          1: [(2, (A1, b1)), (3, (A2, b2))],
                          2: [(1, (A3, b3))]
                      }
        probs (dict): Optional dictionary mapping each vertex to a list of probabilities for each edge.
                      If None, equal probabilities are assumed.
        
        Usage:
        Instead of providing functions for edges, provide (A, b) pairs. The class constructs the affine maps internally.
        """
        self.d = d
        self.vertices = list(range(1, n+1))
        self.edges = edges

    
    def contraction(self, Ks):
        """
        Apply the GD-IFS contraction F to a list of sets Ks = [K1, ..., Kn].

        Ks: list of length n, where Ks[i] is a numpy array of shape (m_i, d) representing points in K_i.

        Returns: list of length n with the updated sets.
        """
        new_Ks = []
        for i in self.vertices:
            points = []
            for j in self.vertices:
                for edge in self.edges[i]:
                    target, (A, b) = edge
                    if target == j:
                        # Apply affine map to all points in K_j
                        K_j = Ks[j - 1]  # vertex indexing starts at 1
                        mapped = (A @ K_j.T).T + b  # shape (m_j, d)
                        points.append(mapped)
            new_Ks.append(np.vstack(points))
            
        return new_Ks

    def draw(self, vertex: int, iter, rotate_angle=0.0, ax = None, **plot_kwargs):

        if ax is None:
            fig, ax = plt.subplots()

        # Initialize Ks with the origin for each vertex
        Ks = [np.array([[0.0, 0.0]]) for _ in self.vertices]
                # Apply contraction iter times
        for _ in range(iter):
            Ks = self.contraction(Ks)

        # Plot the points of the specified vertex
        points = Ks[vertex - 1]  # vertex indexing starts at 1

        # Optionally rotate points through rotate_angle
        if rotate_angle != 0.0:
            c, s = np.cos(rotate_angle), np.sin(rotate_angle)
            R = np.array([[c, -s], [s, c]])
            points = (R @ points.T).T

        ax.scatter(points[:, 0], points[:, 1], **plot_kwargs)

        return ax
        
