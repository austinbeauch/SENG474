import uuid
import time
import re
from pprint import pprint
from random import shuffle

import fnv


p = 15373875993579943603
x = 0.6
s = 14
r = 6


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f s' % \
                  (method.__name__, (te - ts)))
        return result
    return timed

def get_qid_question(line):
	qid, question = line.split("\t")
	question = re.sub(r'[^a-zA-Z0-9 ]+', r'', question)
	question = question.lower()
	return qid, question

@timeit
def ground_set(lines):
	"""Creates ground set of all unique words given in lines"""
	u = set()
	for line in lines[1:]:
			try:
				qid, question = get_qid_question(line)
				u.update(question.split())
			except ValueError:
				continue
	return sorted(list(u))

@timeit
def main(lines):
	a = [uuid.uuid4().int & (1<<64)-1 for i in range(0, s)]
	b = [uuid.uuid4().int & (1<<64)-1 for i in range(0, s)]
	U = ground_set(lines)

	m = 1
	for line in lines[1:]:
		try:
			qid, question = get_qid_question(line)
			for word in question.split():
				hashcode = fnv.hash(word.encode("utf-8"), bits=64)

		except ValueError:
			continue
	return m

def hash_function(a, b, fnvh):
	hf = (a * fnvh + b) % p
	return hf

if __name__ == "__main__":
	n = "150"
	fpath = "../data/question_{}k.tsv".format(n)
	l = [line.rstrip("\n")for line in open(fpath, encoding = "utf8")]
	m = main(l)
