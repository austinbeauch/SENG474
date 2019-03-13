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
    data = [line.split() for line in lines]
    return data

def output(nodes, num):
	with open(r"deadends_{}k.txt".format(num), "w+") as out_file:
		for node in nodes:
			out_file.write("{}\n".format(node))

