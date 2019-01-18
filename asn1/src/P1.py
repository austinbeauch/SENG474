import re
import time
import csv
from copy import deepcopy
from pprint import pprint


# https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
def get_jaccard_sim(str1, str2): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def matrix(d, eps):
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
            f.write("{}\t{}\n".format(key, value))


if __name__ == "__main__":
    n = "4"
    fpath = "../data/question_{}k.tsv".format(n)
    lines = [line.rstrip("\n") for line in open(fpath, encoding="utf8")]
    
    words = []
    data = {}
    word_freq = {}
    for i in lines[1:]:
        try:
            qid, question = i.split("\t")
            question = re.sub(r'[^a-zA-Z0-9 ]+', r'', question)
            question = question.lower()
            data[qid] = question
        except ValueError:
            continue
    pprint(data)
    
    e = 0.6
    
    s = matrix(data, e)
    make_dict(s, n)
