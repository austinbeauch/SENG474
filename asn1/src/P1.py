import sys
import time
import csv
from copy import deepcopy
from pprint import pprint

from utils import jaccard_sim, get_qid_question, timeit, make_dict


def matrix(d, x):
    similar_qids = {}

    for qid1 in d:
        similar_qids[qid1] = ""
        q1 = d[qid1]

        for qid2 in d:
            if qid1 == qid2: 
                continue

            q2 = d[qid2]
            sim = jaccard_sim(q1, q2)
            if sim >= x:
                similar_qids[qid1] += str(qid2) if similar_qids[qid1] == "" else "," + str(qid2)
    
    return similar_qids


@timeit
def main(n, fpath):
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
    
    x = 0.6
    s = matrix(data, x)
    make_dict(s, n)


if __name__ == "__main__":
    try:
        n = sys.argv[1]
    except IndexError:
        n = "4"

    f = "../data/question_{}k.tsv".format(n)
    main(n, f)
