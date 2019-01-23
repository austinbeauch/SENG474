import uuid
import time
from pprint import pprint
from random import shuffle

import fnv
from utils import timeit


p = 15373875993579943603
x = 0.6
s = 14
r = 6


def hash_function(a, b, word):
	encoded_word = fnv.hash(word.encode("utf-8"), bits=64)
	hf = (a * encoded_word + b) % p
	return hf


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


def build_table(lines, U):
	A = [uuid.uuid4().int & (1<<64)-1 for i in range(r)]
	B = [uuid.uuid4().int & (1<<64)-1 for i in range(r)]
	permutations = [{} for i in range(r)] 

	# hashing each word in ground set, storing in dictionary
	for idx in range(r):
		a = A[idx]
		b = B[idx]
		for word in U:
			h = hash_function(a, b, word)
			permutations[idx][word] = h

	signatures = {}
	questions = {}
	for line in lines[1:]:
		try:
			item_set = set()
			qid, question = get_qid_question(line)
			questions[qid] = question  # store original qid, question
			item_set.update(question.split())  # get unique words
			minhash_vect = []
			
			for i in permutations:
				minhash_vect.append(min([i[item] for item in item_set]))  # computre minhash signature
			
			signatures[qid] = minhash_vect  # store minhash signature in signature dict at key qid
		
		except ValueError:
			continue

	return signatures


@timeit
def main(path):
	lines = [line.rstrip("\n")for line in open(path, encoding = "utf8")]
	U = ground_set(lines)

	D = {}
	for i in range(s):
		D[i] = build_table(lines, U)


if __name__ == "__main__":
	n = "4"
	fpath = "../data/question_{}k.tsv".format(n)

	main(fpath)
