import sys
import time
from pprint import pprint

import numpy as np

from utils import timeit, lines, output, output_page_rank
from Q1 import find_dead_ends


T = 10
beta = 0.85


def build_graphs(data):
    outgoing = {}
    incoming = {}

    for node1, node2 in data:
        node1 = int(node1)
        node2 = int(node2)
        if node1 not in outgoing:
            outgoing[node1] = {node2}
        else:
            outgoing[node1].add(node2)
        if node2 not in outgoing:
            outgoing[node2] = set()

        if node2 not in incoming:
            incoming[node2] = {node1}
        else:
            incoming[node2].add(node1)
        if node1 not in incoming:
            incoming[node1] = set()
    
    return outgoing, incoming


def page_rank(outgoing_graph, incoming_graph, dead_ends):
    n = len(outgoing_graph) - len(dead_ends)
    initial_rank = 1 / n
    v = dict()
    v_tmp = dict()
    
    # initialize all pageranks
    for node in outgoing_graph:
        v[node] = initial_rank

    for _ in range(T):
        for i in outgoing_graph:
            if i in dead_ends:
                continue

            incoming = incoming_graph[i].difference(dead_ends)
            summation = 0
            for j in incoming:

                out_deg_j = len(outgoing_graph[j].difference(dead_ends))
                summation += v[j] / out_deg_j
            
            v_tmp[i] = beta * summation + (1 - beta) * initial_rank

        for key in v_tmp:
            v[key] = v_tmp[key]

    return v

@timeit
def page_rank_with_dead_ends(outgoing_graph, incoming_graph, dead_ends_ordered):
    dead_ends = set(np.hstack(dead_ends_ordered))
    v = page_rank(outgoing_graph, incoming_graph, dead_ends)
    for end in dead_ends_ordered[::-1]:
        end = set(end)
        dead_ends = dead_ends.difference(end)
        for i in end:
            summation = 0
            incoming = incoming_graph[i].difference(dead_ends)
            for j in incoming:
                out_deg_j = len(outgoing_graph[j])
                summation += v[j] / out_deg_j
            
            v[i] = summation
    return v


def main(fname):
    print(fname)
    file_path = "../data/{}.txt".format(fname)
    data = lines(file_path)

    outgoing_graph, incoming_graph = build_graphs(data)

    dead_ends_ordered = find_dead_ends(outgoing_graph)
    v = page_rank_with_dead_ends(outgoing_graph, incoming_graph, dead_ends_ordered)
    output_page_rank(v, "10" if len(outgoing_graph) == 10000 else "800")


if __name__ == "__main__":
    main("toy")
    print()
    main("web-Google_10k")
    print()
    main("web-Google")
