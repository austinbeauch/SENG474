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
    return points, features, headings


def loss_func(x, y, w):
    n = len(x)

    total = 0
    for yi, xi in zip(y, x):
        total += (yi - w.T @ xi)**2
    return total / (2 * n)

    # return np.sum((y - w.T @ x)**2) / (2 * n)

def output(n_samples, n_features, points, features, weights, headings):
    with open(r"out.tsv", "w+") as out_file:
        out_file.write("{}\n{}\n{}\n".format(n_samples, n_features, headings))

        for p, f in zip(points, features):
            out_file.write("{}\t".format(p))
            regressed = f * weights
            for r in regressed:
                out_file.write("{}\t".format(int(r)))
            out_file.write("\n")
