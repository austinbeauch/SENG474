import sys
from pprint import pprint

import numpy as np

from utils import timeit, loss_func, tsv_points_features, output


@timeit
def main(n_samples, n_features):
    data_path = "../data/data_{}k_{}.tsv".format(n_samples, n_features)
    n_samples *= 1000
    points, features, headings = tsv_points_features(data_path)

    print(features.shape)

    y = points
    X = features

    w = np.linalg.inv(X.T @ X) @ (X.T @ y)

    loss = loss_func(X, y, w)
    print("Loss:", loss)

    # n_samples, n_features, points, features, weights, headings
    output(n_samples, n_features, points, features, w, headings)


if __name__ == "__main__":
    try:
        n, f = sys.argv[1], sys.argv[2]
    except IndexError:
        n = "100"
        f = "300"
    main(n, f)
