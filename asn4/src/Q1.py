import sys
import time
import copy
from pprint import pprint

import numpy as np
np.random.seed(420)

from utils import *


T = 5


def get_sparse(d, n, m, user_id, movie_id):

    matrix = np.full((n, m), float('nan'))

    # N_j[movie] = users
    N_j = dict()

    # N_i[user] = movies
    N_i = dict()

    for line in d:
        user, movie, rating = line[:3]
        i = np.where(user_id==user)[0][0]
        j = np.where(movie_id==movie)[0][0]
       
        if movie not in N_j:
            N_j[movie] = []
        N_j[movie].append(user)

        if user not in N_i:
            N_i[user] = []
        N_i[user].append(movie)

        # matrix
        matrix[i][j] = rating

    # return user_movie_rating
    return matrix, N_j, N_i

def eq_24(i, k, N_i, U, V, M, user_id, movie_id):
    # i = person
    # j = movie
    numer = 0
    denom = 0

    for movie in N_i[user_id[i]]:
        j = np.where(movie_id==movie)[0][0]
        U_k = np.delete(U[i], k)  # with k element removed
        V_k = np.delete(V[:, j], k)  # taking column vector
        numer += (U_k @ V_k - M[i][j]) * V[k][j] 
    
    for movie in N_i[user_id[i]]:
        j = np.where(movie_id==movie)[0][0]
        denom += V[k][j]**2

    xi = - numer / denom
    return xi


def eq_25(j, k, N_j, U, V, M, user_id, movie_id):
    # i = movie
    # j = user that rated movie i
    numer = 0
    denom = 0

    for user in N_j[movie_id[j]]:
        i = np.where(user_id==user)[0][0]
        U_k = np.delete(U[i], k)  # with k element removed
        V_k = np.delete(V[:, j], k)  # taking column vector
        numer += (U_k @ V_k - M[i][j]) * U[i][k] 
    
    for user in N_j[movie_id[j]]:
        i = np.where(user_id==user)[0][0]  
        denom += U[i][k]**2

    yi = - numer / denom
    return yi


def uv_decomposition(M, n, m, d, N_j, N_i, user_id, movie_id):
    u = np.random.random_sample((n, d))
    v = np.random.random_sample((d, m))

    for _ in range(T):
        for k in range(d):
            x = []
            for i in range(n): # not , before unique 0,1,2,3,...
                x.append(eq_24(i, k, N_i, u, v, M, user_id, movie_id))
            for i in range(n):
                u[i][k] = x[i]

            y = []
            for j in range(m):
                y.append(eq_25(j, k, N_j, u, v, M, user_id, movie_id))
            for j in range(m):
                v[k][j] = y[j]
            print(k)

    return u, v

@timeit
def main(fname="u.data"):
    # fname = "toy_rating.data"
    file_path = "../data/{}".format(fname)
    data = lines(file_path)
    data = np.array(data, dtype=np.int32)

    user_id = data.T[0]  
    movie_id = data.T[1]
    rating = data.T[2]
    
    user_id = np.unique(user_id)
    movie_id = np.unique(movie_id)
    
    m = len(movie_id)
    n = len(user_id)

    print(m, n)

    M, N_j, N_i = get_sparse(data, n, m, user_id, movie_id)

    d = 20
    U, V = uv_decomposition(M, n, m, d, N_j, N_i, user_id, movie_id)

    print(M)
   
    predicted = U @ V
    print(predicted)
    rmse = np.sqrt(np.nanmean((M - predicted)**2))
    print(m)

    print("RMSE:", rmse)

if __name__ == "__main__":
    # main("toy_rating.data")
    main()
