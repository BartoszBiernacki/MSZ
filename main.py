from pyparsing import results

from model import Model
from visualizer import Visualizer
import cProfile
import pstats

if __name__ == '__main__':
    with cProfile.Profile() as profile:

        params = {
            'm0': 4,
            'm': 2,
            'w0': 1,
            'delta': 9,
            'T': 6,
        }

        # connections = Model(**params).run()
        connections = Model(**params).run()
        vis = Visualizer(connection_matrix=connections)

        # vis.node_degrees()

        # -----------------------------------------------------------------
        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.CUMULATIVE)
        results.print_stats(5)
