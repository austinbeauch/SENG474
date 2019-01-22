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
	A = [uuid.uuid4().int & (1<<64)-1 for i in range(r)]
	B = [uuid.uuid4().int & (1<<64)-1 for i in range(r)]
	
	permutations = [{} for i in range(r)] 

	U = ground_set(lines)
	n = len(U)

	for idx in range(r):
		a = A[idx]
		b = B[idx]
		for word in U:
			h = hash_function(a, b, word)
			permutations[idx][word] = h

	m = 1
	signatures = {}
	for line in lines[1:]:
		try:
			item_set = set()
			qid, question = get_qid_question(line)
			item_set.update(question.split())
			minhash_vect = []
			for i in permutations:
				minhash_vect.append(min([i[item] for item in item_set]))
			signatures[qid] = minhash_vect

		except ValueError:
			continue

	for i in signatures:
		for j in signatures:
			if i == j:
				continue
			if signatures[i] == signatures[j]:
				print(i, j)

	return m

def hash_function(a, b, word):
	encoded_word = fnv.hash(word.encode("utf-8"), bits=64)
	hf = (a * encoded_word + b) % p
	return hf

if __name__ == "__main__":
	n = "4"
	fpath = "../data/question_{}k.tsv".format(n)
	l = [line.rstrip("\n")for line in open(fpath, encoding = "utf8")]
	m = main(l)
