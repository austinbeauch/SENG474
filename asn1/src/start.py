import time
import csv
from copy import deepcopy

import pandas as pd

from similarities import get_jaccard_sim


def matrix(df, eps):
    d = df.to_dict()['question']
    d2 = deepcopy(d)

    sims = {}
    start = time.time()
    for i in d:
        sims[i] = ""
        q1 = d[i]
        # del d2[i]

        for j in d2:
            q2 = d2[j]
            sim = get_jaccard_sim(q1, q2)
            if sim >= eps:
                sims[i] += str(j) if sims[i] == "" else "," + str(j)
    
    print("Loop time:", time.time() - start)
    return sims

def make_dict(d, n):
    with open(f"question_sim_{n}k.tsv", "w+") as f:
        f.write("qid\tsimilar-qids\n")
        for key in d:
            val = d[key]
            f.write(f"{key}\t{val}\n")


if __name__ == "__main__":
    n = "10"
    fpath = f"../data/question_{n}k.tsv"
    data = pd.read_table(fpath, index_col=0)

    e = 0.6
    
    s = matrix(data, e)
    make_dict(s, n)
