import sys
import time
from pprint import pprint

import numpy as np

from utils import timeit, lines, output
from Q1 import build_graph, find_dead_ends


T = 1
beta = 0.85


def page_rank(graph):
    n = len(graph)
    initial_rank = 1 / n
    v = dict()
    
    # initialize all pageranks
    for node in graph:
        v[node] = initial_rank


    for _ in range(T):
        for i in graph:
            outgoing = graph[i]
            summation = 0
            for j in outgoing:
                v_j = v[j]
                out_deg_j = len(graph[j])
                summation += (v_j / out_deg_j) + ((1 - beta) * initial_rank)
            v[i] = beta * summation

    return v

@timeit
def page_rank_with_dead_ends(graph, deadless_graph, dead_ends_ordered):
    v = page_rank(deadless_graph)
    dead_ends = set(np.hstack(dead_ends_ordered))
    return
    # insert recently removed guys
    print(set(dead_ends))
    # print(dead_ends_ordered)
    # print(graph)
    # print(deadless_graph)
    # print()

    for end in dead_ends_ordered[::-1]:
        print(end)
        end = set(end)
        dead_ends = dead_ends.difference(end)

        # computre page rank for dead ends in order
        # for dead in end:
        #  computre v[i] shit

    return v


def main(fname):
    print(fname)
    file_path = "../data/{}.txt".format(fname)
    data = lines(file_path)

    graph = build_graph(data)
    dead_ends_ordered, deadless_graph = find_dead_ends(graph)

    v = page_rank_with_dead_ends(graph, deadless_graph, dead_ends_ordered)


if __name__ == "__main__":
    # main("toy")
    print()
    main("web-Google_10k")
    print()
    main("web-Google")
