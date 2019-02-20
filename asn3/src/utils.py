import time

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
    data = np.array(data, dtype=int)
    return data
