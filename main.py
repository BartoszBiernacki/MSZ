from model import Model
from visualizer import Visualizer
import cProfile
import pstats

timeit = False


def main():
    params = {
        'm0': 4,
        'm': 2,
        'w0': 1,
        'delta': 9,
        'T': 10,
    }

    connections = Model(**params).run()
    vis = Visualizer(connection_matrix=connections)
    # vis.node_degrees()

if __name__ == '__main__':
    with cProfile.Profile() as profile:
        main()

        # -----------------------------------------------------------------
        results = pstats.Stats(profile)
        results.sort_stats(pstats.SortKey.CUMULATIVE)

        if timeit:
            results.print_stats(5)

