import sys
import time
from pprint import pprint

import numpy as np

from utils import timeit, lines, output


def find_dead_ends(graph):
    dead_end = set()        
    while True:
        # first pass finding all nodes with no outgoing edge
        updated = False
        for node in graph:
            if len(graph[node]) == 0:
                if node not in dead_end:
                    updated = True
                dead_end.add(node)

        # second pass finding all nodes whose outgoing edges are all to dead ends
        for node in graph:
            if graph[node].issubset(dead_end):
                if node not in dead_end:
                    updated = True
                dead_end.add(node)
        if not updated:
            break
    return dead_end


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


@timeit
def main(fname):
    file_path = "../data/{}.txt".format(fname)
    data = lines(file_path)

    graph = build_graph(data)
    dead_ends = find_dead_ends(graph)
    
    print(len(dead_ends), "dead ends")
    
    output(sorted(dead_ends), "10" if len(graph) == 10000 else "800")

if __name__ == "__main__":
    main("web-Google_10k")
    main("web-Google")
