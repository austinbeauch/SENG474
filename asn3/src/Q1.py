import sys
import time
from pprint import pprint

import numpy as np

from utils import timeit, lines


@timeit
def main(fname):
    file_path = "../data/{}.txt".format(fname)
    data = lines(file_path)

    edges = {}
    for node1, node2 in data:
        if node1 not in edges:
            edges[node1] = [node2]
        else:
            edges[node1].append(node2)
        if node2 not in edges:
            edges[node2] = []
    
    # print(edges)
    print("Built")

    dead_end = []
    while True:
        updated = False
        new_dead = []

        start = time.time()
        for node in edges:
            outgoing = edges[node]
            
            if len(outgoing) == 0:
                updated = True
                dead_end.append(node)
                new_dead.append(node)
        
        print("Loop1", time.time()-start)
        
        if not updated:
            break
    
        start = time.time()
        edges = dict([(k, v) for k, v in edges.items() if len(v) > 0])
        print("Loop2", time.time()-start)
        
        start = time.time()
        # this takes way too long on the full set
        # baseline 31s with printing
        for i, node in enumerate(edges):
            # print(i)
            try:
                # exemaple removal, need to remove every previously removed dead end
                # edges[node] = list(set(edges[node]).difference(new_dead)) -> too long
                edges[node].remove(5)
            except:
                pass
        print("Loop3", time.time()-start)

    print(len(dead_end))


if __name__ == "__main__":
    try:
        x = sys.argv[1]
    except IndexError:
        x = "toy"
    main(x)
