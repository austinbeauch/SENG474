import sys
from pprint import pprint

import numpy as np

from utils import timeit, loss_func, output


@timeit
def main(n_samples, n_features):
    data_path = "../data/data_{}k_{}.tsv".format(n_samples, n_features)
    print(data_path)

    lines = [line.rstrip("\n") for line in open(data_path, encoding="utf8")]
    n_samples, n_features = lines[:2]

    
    data = [line.split("\t") for line in lines[3:]]
    data = np.array(data, dtype=float)
    
    points = data[:, 0]
    features = data[:, 1:]
    
    print(features.shape)

    y = points
    X = features

    w = np.linalg.inv(X.T @ X) @ (X.T @ y)

    loss = loss_func(X, y, w)
    print("Loss:", loss)


if __name__ == "__main__":
    try:
        n, f = sys.argv[1], sys.argv[2]
    except IndexError:
        n = "100"
        f = "300"
    main(n, f)
