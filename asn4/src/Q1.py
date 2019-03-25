import sys
import time
import copy
from pprint import pprint

import numpy as np
np.random.seed(420)

from utils import *


T = 5

@timeit
def get_sparse(d, n, m):
    matrix = np.full((n, m), float('nan'))
    
    # Where N(j) is the set of users that rate item j.
    N_j = []

    # N_i[user] = movies
    N_i = []

    user_index = 0
    movie_index = 0

    users = dict()
    movies = dict()

    for line in d:
        user, movie, rating = line[:3]

        if user not in users:
            users[user] = user_index
            user_index += 1
        if movie not in movies:
            movies[movie] = movie_index
            movie_index += 1       
        
        try:
            N_j[movie].append(user)
        except IndexError:
            N_j.append([user])

        try:
            N_i[user].append(movie)
        except IndexError:
            N_i.append([movie])

        matrix[users[user]][movies[movie]] = rating

    N_j = np.array([np.array(i) for i in N_j])
    N_i = np.array([np.array(i) for i in N_i])

    return matrix, N_j, N_i, movies, users

def eq_24(i, k, N_i, U, V, M, user):
    numer = 0
    denom = 0
    print(N_i)
    exit()
    # Where N(i) is the set of movies that got rated by user i
    # for j in N(i)
    for movie in N_i[user]:
        print(i)
        print(users[i])
        print(movie)
        exit()
        # find j
        j = 0
        numer += ((U[i] @ V[j] - U[i][k]*V[k][j]) - M[i][j]) * V[k][j] 
    
    for movie in N_i[users[i]]:
        denom += V[k][j]**2

    xi = - numer / denom
    return xi


def eq_25(j, k, N_j, U, V, M, movies, users):
    # i = movie
    # j = user that rated movie i
    numer = 0
    denom = 0

    for user in N_j[movie_id[j]]:
        numer += ((U[i] @ V[j] - U[i][k]*V[k][j]) - M[i][j]) * U[i][k] 
    
    for user in N_j[movie_id[j]]:
        i = np.where(user_id==user)[0][0]  
        denom += U[i][k]**2

    yi = - numer / denom
    return yi


def uv_decomposition(M, n, m, d, N_j, N_i, movies, users):
    u = np.random.random_sample((n, d))
    v = np.random.random_sample((d, m))

    for _ in range(T):
        for k in range(d):
            x = []
            for user in users:
                # i represents the index for that user
                i = users[user]
                x.append(eq_24(i, k, N_i, u, v, M, user))
            for i in range(n):
                u[i][k] = x[i]

            # y = []
            # for j in range(m):
            #     y.append(eq_25(j, k, N_j, u, v, M, users, movies))
            # for j in range(m):
            #     v[k][j] = y[j]
            # print(k)

    return u, v

@timeit
def main(fname="u.data"):
    fname = "toy_rating.data"
    file_path = "../data/{}".format(fname)
    data = lines(file_path)
    data = np.array(data, dtype=np.int32)

    user_id = data.T[0]  
    movie_id = data.T[1]
    
    user_id = np.unique(user_id)
    movie_id = np.unique(movie_id)
    
    m = len(movie_id)
    n = len(user_id)
    print(f"n {n}, m {m}")

    M, N_j, N_i, movies, users = get_sparse(data, n, m)

    d = 20
    U, V = uv_decomposition(M, n, m, d, N_j, N_i, movies, users)

    print(M)
   
    predicted = U @ V
    print(predicted)
    rmse = np.sqrt(np.nanmean((M - predicted)**2))

    print("RMSE:", rmse)

if __name__ == "__main__":
    main()
