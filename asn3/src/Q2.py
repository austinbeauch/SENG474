import sys
import time
from pprint import pprint

import numpy as np

from utils import timeit, lines, output
from Q1 import build_graph, find_dead_ends


def page_rank(graph):
    n = len(graph)
    v = 1/n * np.ones((int(n)))

    beta = 0.85
    for i in range(n):
        summation = 0
        for j in range(n):
            try:
                summation += (v[j] / len(graph[j])) + (1 - beta) * (1 / n)
            except KeyError:
                pass

        v[i] = beta * summation

    return v


def page_rank_with_dead_ends(graph, deadless_graph, dead_ends_ordered):
    v = 1 # page_rank(deadless_graph)

    # insert recently removed guys
    # print(dead_ends_ordered)
    # print(deadless_graph)
    print()

    for dead_end in dead_ends_ordered[::-1]:
        print(dead_end)

    return v


def main(fname):
    print(fname)
    file_path = "../data/{}.txt".format(fname)
    data = lines(file_path)

    graph = build_graph(data)
    dead_ends_ordered, deadless_graph = find_dead_ends(graph)

    v = page_rank_with_dead_ends(graph, deadless_graph, dead_ends_ordered)


if __name__ == "__main__":
    main("toy")
    print()
    # main("web-Google_10k")
    print()
    # main("web-Google")
