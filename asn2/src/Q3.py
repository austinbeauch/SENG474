import sys
from pprint import pprint

import numpy as np
np.random.seed(69)
from matplotlib import pyplot as plt


from utils import timeit, loss_func, tsv_points_features, output


def stochastic_gradient_descent(n_features, n, X, y):
    m = 1
    if n_features == 101:
        T = 20
        ada = 0.000001
    elif n_features == 301:
        T = 12
        ada = 0.0000001
    
    w = np.random.random_sample(n_features)
    
    for _ in range(T):
        randomize = np.arange(len(X))
        np.random.shuffle(randomize)
        XX = X[randomize]
        yy = y[randomize]
        XX = np.split(XX, n / m)
        yy = np.split(yy, n / m)

        for label, features in zip(yy, XX):
            xp = features[0]
            yp = np.array(list(label) * n_features)
            yp_hat = np.array([w.T @ xp] * n_features)
            w = w + (ada / m) * ((yp - yp_hat) * xp)
    
    return w


@timeit
def main(n_samples, n_features):
    data_path = "../data/data_{}k_{}.tsv".format(n_samples, n_features)
    n_samples *= 1000

    
    points, features, headings = tsv_points_features(data_path)
    n_features = features.shape[-1]
    y = points
    X = features

    w = stochastic_gradient_descent(n_features, n_samples, X, y)

    loss = loss_func(X, y, w)
    print("Loss {} samples: {}".format(n_samples, loss))

    output(w, "Q3")


if __name__ == "__main__":
    n = 10
    f = 100
    main(n, f)
    
    n = 100
    f = 300
    main(n, f)
