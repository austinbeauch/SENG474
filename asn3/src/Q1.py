import sys
import time
import copy
from pprint import pprint

import numpy as np

from utils import timeit, lines, output


def build_graph(data):
    graph = {}
    for node1, node2 in data:
        node1 = int(node1)
        node2 = int(node2)
        if node1 not in graph:
            graph[node1] = {node2}
        else:
            graph[node1].add(node2)
        if node2 not in graph:
            graph[node2] = set()
    return graph


def find_dead_ends(graph):
    dead_end = set() 
    dead_end_ordered = []

    # first pass finding all nodes with no outgoing edge      
    order_1 = []
    for node in graph:
        if len(graph[node]) == 0 and node not in dead_end:
            dead_end.add(node)  
            order_1.append(node)
    
    if len(order_1) > 0:
        dead_end_ordered.append(order_1)

    while True:    
        updated = False

        # second pass finding all nodes whose outgoing edges are all to dead ends
        next_removal = []
        for node in graph:
            if graph[node].issubset(dead_end) and node not in dead_end:
                updated = True
                dead_end.add(node)
                next_removal.append(node)

        if not updated:
            break

        dead_end_ordered.append(next_removal)
    
    return dead_end_ordered 


@timeit
def main(fname):
    file_path = "{}.txt".format(fname)
    data = lines(file_path)

    graph = build_graph(data)

    dead_ends = find_dead_ends(graph)
    # print(dead_ends)
    dead_ends = np.hstack(dead_ends)

    print(len(dead_ends), "dead ends")

    output(sorted(dead_ends), "10" if len(graph) == 10000 else "800")

if __name__ == "__main__":
    main("web-Google_10k")
    main("web-Google")
