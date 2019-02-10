import sys
from pprint import pprint

import numpy as np
from matplotlib import pyplot as plt


from utils import timeit, loss_func, tsv_points_features, output


def stochastic_gradient_descent(n_features, n, X, y):
    m = 1
    if n_features == 100:
        T = 20
        ada = 0.000001
    else:
        T = 12
        ada = 0.0000001
    
    w = np.random.random_sample(n_features)*10
    w_history = []
    for _ in range(T):
    
        #randomize = np.arange(len(X))
        #np.random.shuffle(randomize)
        
        #XX = X[randomize]
        #yy = y[randomize]
    
        XX = np.split(X, n / m)
        yy = np.split(y, n / m)

        for label, features in zip(yy, XX):
            xp = features[0]
            yp = label
            for j in range(n_features):
                if j == 0:
                    w_history.append(w[j])
                yp_hat = w.T @ xp
                w[j] = w[j] + ada*((yp - yp_hat)*xp[j]) 
    
    
    plt.plot([i for i in range(n*T)], w_history, '.')
    plt.show()
    
    return w


@timeit
def main(n_samples, n_features):
    if True:
        data_path = "../data/data_{}k_{}.tsv".format(n_samples, n_features)
        n_samples *= 1000
    else:
        data_path = "../data/pa2-sample.tsv"
        n_samples = 4
        n_features = 2
    
    points, features, headings = tsv_points_features(data_path)

    y = points
    X = features

    w = stochastic_gradient_descent(n_features, n_samples, X, y)

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
