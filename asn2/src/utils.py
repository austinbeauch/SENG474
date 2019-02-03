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


def loss_func(x, y, w):
    n = len(x)

    total = 0
    for yi, xi in zip(y, x):
        total += (yi - w.T @ xi)**2
    return total / (2 * n)

    # return np.sum((y - w.T @ x)**2) / (2 * n)
