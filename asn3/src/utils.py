import time
import operator

import numpy as np


def timeit(method):
	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()
		print('%r  %2.2f s' % \
				(method.__name__, (te - ts)))
		return result
	return timed

def lines(path):
    lines = [line.rstrip("\n") for line in open(path, encoding="utf8")]
    metadata = lines[:3]
    data = [line.split() for line in lines[4:]]
    return data

def output(nodes, num):
	with open(r"deadends_{}k.txt".format(num), "w+") as out_file:
		for node in nodes:
			out_file.write("{}\n".format(node))

def output_page_rank(ranks, num):
	sorted_ranks = sorted(ranks.items(), key=lambda kv: kv[1], reverse=True)
	with open(r"PR_{}k.txt".format(num), "w+") as out_file:
		out_file.write("PageRank\tIds\n")
		for node, rank in sorted_ranks:
			out_file.write("{}\t{}\n".format(rank, node))
