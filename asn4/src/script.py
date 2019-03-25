import sys
import time
import copy
from pprint import pprint

import numpy as np
np.random.seed(420)

from utils import *


T = 20
d = 20

### MAIN ###
fname="u.data"
# fname = "toy_rating.data"
file_path = "../data/{}".format(fname)
data = lines(file_path)
data = np.array(data, dtype=np.int32)

user_id = data.T[0]  
movie_id = data.T[1]

user_id = np.unique(user_id)
movie_id = np.unique(movie_id)

m = len(movie_id)
n = len(user_id)

U = np.random.random_sample((n, d))
V = np.random.random_sample((d, m))
### MAIN ###


### GET SPARSE ####
M = np.full((n, m), float('nan'))

# Where N(j) is the set of users that rate item j.
N_j = []

# N_i[user] = movies
N_i = []

user_index = 0
movie_index = 0

users = dict()
movies = dict()

for line in data:
    user, movie, rating = line[:3]

    if user not in users:
        users[user] = user_index
        user_index += 1
    if movie not in movies:
        movies[movie] = movie_index
        movie_index += 1       
    
    try:
        N_j[movies[movie]].append(user)
    except IndexError:
        N_j.append([user])

    try:
        N_i[users[user]].append(movie)
    except IndexError:
        N_i.append([movie])

    M[users[user]][movies[movie]] = rating

# N_j = np.array([np.array(i) for i in N_j])
# N_i = np.array([np.array(i) for i in N_i])

### GET SPARSE ####

def eq_24(user, k):
    numer = 0
    denom = 0

    # i is the index for that user
    i = users[user]

    # Where N(i) is the set of movies that got rated by user i
    for movie in N_i[i]:
        j = movies[movie]
        numer += ((U[i] @ V[:, j] - U[i][k]*V[k][j]) - M[i][j]) * V[k][j] 

    for movie in N_i[i]:
        j = movies[movie]
        denom += V[k][j]**2

    xi = - numer / denom
    return xi


def eq_25(movie, k):
    j = movies[movie]
    numer = 0
    denom = 0

    for user in N_j[j]:
        i = users[user]
        numer += ((U[i] @ V[:, j] - U[i][k]*V[k][j]) - M[i][j]) * U[i][k] 
    
    for user in N_j[j]:
        i = users[user]
        denom += U[i][k]**2

    yi = - numer / denom
    return yi


def uv_decomposition():
    for t in range(T):
        for k in range(d):
            x = []
            for user in users:
                # sending the current user_id
                x.append(eq_24(user, k))

            for i in range(n):
                U[i][k] = x[i]

            y = []
            for movie in movies:
                y.append(eq_25(movie, k))

            for j in range(m):
                V[k][j] = y[j]

full_start = time.time()
uv_decomposition()
print("Decomp time:", time.time()-full_start)

predicted = U @ V

rmse = np.sqrt(np.nanmean((M - predicted)**2))

print("RMSE:", rmse)

print(users)
print(U)
print(V)

with open(r"UT.tsv", "w+") as out_file:
    for user in sorted(users):
        out_file.write("{}\t".format(user))
        for d in U[users[user]]:
            out_file.write("{}\t".format(d))
        out_file.write("\n")

with open(r"VT.tsv", "w+") as out_file:
    for movie in sorted(movies):
        out_file.write("{}\t".format(movie))
        for d in V.T[movies[movie]]:
            out_file.write("{}\t".format(d))
        out_file.write("\n")