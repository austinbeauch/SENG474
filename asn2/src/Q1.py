import sys
from pprint import pprint

import numpy as np

from utils import timeit, loss_func, tsv_points_features, output


@timeit
def main(n_samples, n_features):
    data_path = "data_{}k_{}.tsv".format(n_samples, n_features)
    n_samples *= 1000

    points, features, headings = tsv_points_features(data_path)
    
    n_features = features.shape[-1]

    y = points
    X = features

    w = np.linalg.inv(X.T @ X) @ (X.T @ y)

    loss = loss_func(X, y, w)
    print("Loss:", loss)

    output(w, "Q1")


if __name__ == "__main__":
    try:
        n, f = int(sys.argv[1]), int(sys.argv[2])
    except IndexError:
        n = "100"
        f = "300"
    main(n, f)
