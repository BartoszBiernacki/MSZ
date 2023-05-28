import numpy as np


class Analyzer:
    def __init__(self, connection_matrix: np.ndarray):
        self.connection_matrix = connection_matrix

    def node_degrees(self) -> np.ndarray:
        return np.count_nonzero(self.connection_matrix, axis=0)

    def node_strengths(self) -> np.ndarray:
        return self.connection_matrix.sum(axis=0)

    def connection_weights(self) -> np.ndarray:
        flat_upper_triangle = np.triu(self.connection_matrix, k=0).flatten()
        idx = np.nonzero(flat_upper_triangle)
        return flat_upper_triangle[idx]
