from model import Model


if __name__ == '__main__':
    params = {
        'm0': 4,
        'm': 2,
        'w0': 1,
        'delta': 9,
        'T': 5,
    }

    Model(**params).run()