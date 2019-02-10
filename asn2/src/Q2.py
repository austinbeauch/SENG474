import sys
from pprint import pprint

import numpy as np

from utils import timeit, loss_func, tsv_points_features, output

T = 200


def gradient_descent(n_features, n, X, y):
    w = np.random.random_sample(n_features)
    ada = 0.000001 
    for _ in range(T):
        w = w - (ada/n * ((X.T @ X @ w) - X.T @ y))
    return w


@timeit
def main(n_samples, n_features):
    data_path = "../data/data_{}k_{}.tsv".format(n_samples, n_features)
    n_samples *= 1000
    points, features, headings = tsv_points_features(data_path)

    y = points
    X = features
    w = gradient_descent(n_features, n_samples, X, y)

    loss = loss_func(X, y, w)
    print("Loss:", loss)

    # n_samples, n_features, points, features, weights, headings
    # output(n_samples, n_features, points, features, w, headings)


if __name__ == "__main__":
    try:
        n, f = int(sys.argv[1]), int(sys.argv[2])
    except IndexError:
        n = 10
        f = 100
    main(n, f)
