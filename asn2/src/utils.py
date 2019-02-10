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


def tsv_points_features(path):
    lines = [line.rstrip("\n") for line in open(path, encoding="utf8")]
    headings = lines[2]
    data = [line.split("\t") for line in lines[3:]]
    data = np.array(data, dtype=float)
    
    points = data[:, 0]
    features = data[:, 1:]
    
    ones = np.ones((len(features), 1))
    features = np.append(features, ones, axis=1)
    
    return points, features, headings


def loss_func(x, y, w):
    n = len(x)

    total = 0
    for yi, xi in zip(y, x):
        total += (yi - w.T @ xi)**2
    return total / (2 * n)

def output(weights, fname):
    with open(r"{}_out.tsv".format(fname), "w+") as out_file:
        for w in range(len(weights))[:-1]:
            out_file.write("w{}\t".format(w + 1))
        out_file.write("w0\n")
        for weight in weights:
            out_file.write("{}".format(weight))
