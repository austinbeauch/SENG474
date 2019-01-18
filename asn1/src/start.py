import time
import csv
from copy import deepcopy
import numpy
import pandas as pd

from similarities import get_jaccard_sim


def matrix(df, eps):
    d = df.to_dict()['question']
    # d2 = deepcopy(d)
	
	

    sims = {}
    start = time.time()
    for i in d:
        sims[i] = ""
        q1 = d[i]
        # del d2[i]

        for j in d:
            if i == j: 
                continue
            q2 = d[j]
            sim = get_jaccard_sim(q1, q2)
            if sim >= eps:
                sims[i] += str(j) if sims[i] == "" else "," + str(j)
    
    print("Loop time:", time.time() - start)
    return sims

def make_dict(d, n):
    with open("question_sim_{}k.tsv".format(n), "w+") as f:
        f.write("qid\tsimilar-qids\n")
        for key in d:
            val = d[key]
            f.write(f"{key}\t{val}\n")


if __name__ == "__main__":
    n = "4"
    fpath = "../data/question_{}k.tsv".format(n)
    data = pd.read_table(fpath, index_col=0)

    e = 0.6
    
    s = matrix(data, e)
    print(numpy.min(np.array(s.values().astype(int))))
    make_dict(s, n)
