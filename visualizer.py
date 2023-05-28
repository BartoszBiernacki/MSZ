import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from analyzer import Analyzer


class Visualizer:
    def __init__(self, connection_matrix: np.ndarray):
        self._anal = Analyzer(connection_matrix=connection_matrix)

    @staticmethod
    def _geo_seq(start: float, stop: float, ratio: float) -> np.ndarray:
        # Calculate the number of elements in the sequence
        num = int(np.ceil(np.log(stop / start) / np.log(ratio))) + 1

        return np.array([start * ratio ** i for i in range(num)])

    def node_degrees(self) -> None:
        distribution = self._anal.node_degrees()

        bins_geo = self._geo_seq(
            start=1,
            stop=distribution.max(), ratio=1.42)

        fig, ax = plt.subplots()
        sns.despine()

        ax.hist(
            x=distribution,
            bins=bins_geo,
            density=True,
            log=True,
        )

        ax.set_xlabel('Stopień węzła, k')
        ax.set_ylabel('P(k)')
        ax.set_xscale('log')
        plt.show()


