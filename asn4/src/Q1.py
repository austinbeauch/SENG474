import sys
import time
import copy
from pprint import pprint

import numpy as np

from utils import *


T = 20


def get_sparse(d, n, m):
    user_movie_rating = dict()

    matrix = np.full((n, m), -1)

    # N[movie] = user
    N = dict()

    for line in d:
        user, movie, rating = line[:3]
        
        # dictionary
        if user not in user_movie_rating:
            user_movie_rating[user] = dict()
        user_movie_rating[user][movie] = rating
        
        if movie not in N:
            # change to dict with rating values if needed
            N[movie] = []
        N[movie].append(user)

        # matrix
        matrix[user][movie] = rating

    # return user_movie_rating
    return matrix, N


def eq_25(i, k, N, U, V, M):
    # i = movie
    # j = user that rated movie i
    for movie in N:
        j = N[movie]
        numer = 0
        denom = 0
        for i in j:
            U_k = np.delete(U[i], k) # with k element removed
            V_k = np.delete(V[j], k)
            numer += (U_k @ V_k - M[i][j]) * U[j][k] 
        for j in i:
            denom += U[i][k]**2
        yi = - numer / denom
    
    return yi


def eq_24(i, k, N, U, V, M):
    # i = movie
    # j = user that rated movie i
    numer = 0
    denom = 0
    print(U.shape, V.shape)
    for j in N[i]:

        U_k = np.delete(U[i], k) # with k element removed
        V_k = np.delete(V[:, j], k)  # taking column vector

        try:
            print(M)
            print(i, j)
            print(M[i][j])
            print()
            numer += (U_k @ V_k - M[i][j]) * V[j][k] 
        except:
            exit()
        
    print("done")
    exit()
    
    return xi


def uv_decomposition(M, n, m, d, N):
    u = np.random.random_sample((n, d))
    v = np.random.random_sample((d, m))

    for _ in range(T):
        for k in range(d):
            x= []

            for i in range(n):
                x.append(eq_24(i, k, N, u, v, M))
            for i in range(n):
                u[i][k] = x[i]
        
        for k in range(d):
            y = []

            for j in range(m):
                y.append(eq_25(i, k, N, u, v, M))
                
            for j in range(n):
                v[k][j] = y[j]

    return u, v

@timeit
def main(fname="u.data"):
    fname = "toy_rating.data"
    file_path = "../data/{}".format(fname)
    data = lines(file_path)
    data = np.array(data, dtype=np.int32)

    user_id = data.T[0]  
    movie_id = data.T[1]
    rating = data.T[2]

    m = movie_id.max() + 1
    n = user_id.max() + 1

    M, N = get_sparse(data, n, m)

    d = 2
    U, V = uv_decomposition(M, n, m, d, N)

if __name__ == "__main__":
    # main("toy_rating.data")
    main()
