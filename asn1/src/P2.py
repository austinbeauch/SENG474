import uuid
import time
import re
from pprint import pprint
from random import shuffle


import fnv

p =	 15373875993579943603
x = 0.6
s = 14
r = 6


def get_qid_question(line):
	qid, question = line.split("\t")
	question = re.sub(r'[^a-zA-Z0-9 ]+', r'', question)
	question = question.lower()
	return qid, question


def ground_set(f):
	u = set()
	lines = [line.rstrip("\n")for line in open(f, encoding = "utf8")]
	for line in lines[1:]:
			try:
				qid, question = get_qid_question(line)
				#for word in question.split():
				u.update(question.split())
			except ValueError:
				continue
	return u

def testing(f):
	a = [uuid.uuid4().int & (1<<64)-1 for i in range(0,14)]
	b = [uuid.uuid4().int & (1<<64)-1 for i in range(0,14)]
	U = ground_set(f)

	lines = [line.rstrip("\n")for line in open(f, encoding = "utf8")]
	m = 1
	for line in lines[1:]:
		try:
			qid, question = get_qid_question(line)

			u = []  # TODO: Make ground set the full set of all words
			for word in question.split():
				hashcode = fnv.hash(word.encode("utf-8"), bits=64)
				u.append(hashcode)
			
			# pi_i = [[i for i in range(len(u))] for _ in range(6)]
			# for i in pi_i:
			# 	shuffle(i)
			# pprint(pi_i)
			# exit()

		except ValueError:
			continue
	return m

def hash_function(a, b, fnvh):
	hf = (a * fnvh + b) % p
	return hf

if __name__ == "__main__":
	n = "4"
	fpath = "../data/question_{}k.tsv".format(n)
	m = testing(fpath)
