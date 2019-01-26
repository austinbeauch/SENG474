import time
import csv
from copy import deepcopy
from pprint import pprint

from utils import jaccard_sim, get_qid_question, timeit


def matrix(d, eps):
    similar_qids = {}

    for qid1 in d:
        similar_qids[qid1] = ""
        q1 = d[qid1]

        for qid2 in d:
            if qid1 == qid2: 
                continue

            q2 = d[qid2]
            sim = jaccard_sim(q1, q2)
            if sim >= eps:
                similar_qids[qid1] += str(qid2) if similar_qids[qid1] == "" else "," + str(qid2)
    
    return similar_qids

    
def make_dict(d, n):
    with open("question_sim_{}k.tsv".format(n), "w+") as f:
        f.write("qid\tsimilar-qids\n")
        for key in d:
            val = d[key]
            f.write("{}\t{}\n".format(key, val))


@timeit
if __name__ == "__main__":
    start = time.time()

    n = "4"
    fpath = "../data/question_{}k.tsv".format(n)
    lines = [line.rstrip("\n") for line in open(fpath, encoding="utf8")]
    
    words = []
    data = {}
    word_freq = {}
    for line in lines[1:]:
        try:
            qid, question = get_qid_question(line)
            data[qid] = question
        except ValueError:
            continue
    
    e = 0.6
    s = matrix(data, e)
    make_dict(s, n)

    print("Runtime:", time.time() - start)
