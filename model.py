from typing import Iterable
from numba import njit, prange, types
import numpy as np


class Model:
    def __init__(
            self,
            m0: int,
            m: int,
            w0: int,
            delta: float,
            T: int,
    ):
        self.m0 = m0
        self.m = m
        self.w0 = w0
        self.delta = delta
        self.t = 0
        self.T = T

        self.num_of_nodes = 0
        self.connections = np.zeros(shape=(m0 + T, m0 + T), dtype=np.float64)

        self._initialize()

    @staticmethod
    @njit("f8[:](f8[:,:])", cache=True, fastmath=True, parallel=True)
    def __normalized_strengths(cons: np.ndarray) -> np.ndarray:
        N = cons.shape[0]
        strengths = np.zeros(N, dtype=np.float64)
        for j in prange(N):
            for i in range(N):
                strengths[j] += cons[j][i]

        return strengths / strengths.sum()

    def _draw_m_nodes(self) -> list[int]:
        existing_connections = self.connections[
                               :self.num_of_nodes, :self.num_of_nodes]

        # Numba outperforms numpy if num of nodes > 2000.
        if self.num_of_nodes < 2000:
            strengths = existing_connections.sum(axis=0)
            normalized_strengths = strengths / strengths.sum()
        else:
            normalized_strengths = self.__normalized_strengths(existing_connections)

        return np.random.choice(
            a=range(self.num_of_nodes),
            size=self.m,
            replace=False,
            p=normalized_strengths,
        )

    def _add_connections(self, new_node: int, existing_nodes: Iterable):
        for j in existing_nodes:
            self.connections[new_node, j] = self.w0
            self.connections[j, new_node] = self.w0

    def _update_connection_weights(self):
        # Update weights of previously existing connections after
        # establishing new connection.
        # First scan all then update, otherwise order of randomly
        # m picked nodes matter, but shouldn't!
        connections_to_increase = []
        increase_values = []
        for j, weight in enumerate(self.connections[self.num_of_nodes]):
            if weight == self.w0:
                column = self.connections[:self.num_of_nodes, j]
                row = self.connections[j, :self.num_of_nodes]

                # with np.printoptions(precision=2, suppress=True):
                #     print(f'{j = }')
                #     print(f'{column = }')
                #     print(f'{row = }')

                increase = self.delta * (column/column.sum())

                connections_to_increase.extend((column, row))
                increase_values.extend((increase, increase))
        for connection, increase in zip(
                connections_to_increase, increase_values):

            connection += increase

    def _initialize(self) -> None:
        for i in range(self.m0):
            for j in range(i + 1, self.m0):
                self._add_connections(i, [j])
        self.num_of_nodes = self.m0

    def show_network(self) -> None:
        pass
        # with np.printoptions(precision=1, suppress=True):
        #     print(f't = {self.t}')
        #     print(self.connections[:self.num_of_nodes, :self.num_of_nodes])
        #     print()

    def step(self) -> None:
        self.show_network()
        self._add_connections(
            new_node=self.num_of_nodes,
            existing_nodes=self._draw_m_nodes(),
        )
        self._update_connection_weights()
        self.num_of_nodes += 1
        self.t += 1

    def run(self):
        self._initialize()

        while self.t < self.T:
            self.step()

        self.show_network()
        return self.connections


