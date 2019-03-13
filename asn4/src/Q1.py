import sys
import time
import copy
from pprint import pprint

import numpy as np

from utils import *


T = 20


def get_sparse(d):
    sparse = dict()

    user_id = d.T[0]  
    movie_id = d.T[1]
    m = movie_id.max()
    n = user_id.max()
    matrix = np.full((n, m), -1)

    # N[movie] = user
    N = dict()

    for line in d:
        user, movie, rating = line[:3]
        
        # dictionary
        if user not in sparse:
            sparse[user] = dict()
        sparse[user][movie] = rating
        
        if movie not in N:
            # change to dict with rating values if needed
            N[movie] = []
        N[movie].append(user)

        # matrix
        user -= 1
        movie -= 1
        matrix[user][movie] = rating

    print(matrix)
    return sparse


def uv_decomposition(M, n, m, d):
    u = np.random.random_sample((n, d))
    v = np.random.random_sample((d, m))
    print(u.shape, v.shape)

    for _ in range(T):
        for k in range(d):
            for i in range(n):
                # eq 24
                pass
            for i in range(n):
                # u[i][k] = x[i]
                pass
        
        for k in range(d):
            for j in range(m):
                # eq 25
                pass
            for j in range(n):
                # v[k][j] = y[j]
                pass

    return u, v

@timeit
def main(fname="u.data"):
    fname = "toy_rating.data"
    file_path = "../data/{}".format(fname)
    data = lines(file_path)
    data = np.array(data, dtype=np.int32)

    sparse = get_sparse(data)

    # user_id = data.T[0]  
    # movie_id = data.T[1]
    # rating = data.T[2]

    # m = movie_id.max()
    # n = user_id.max()

    # d = 20
    # U, V = uv_decomposition(data, n, m, d)

if __name__ == "__main__":
    # main("toy_rating.data")
    main()
