import sys
import uuid
from pprint import pprint
from random import shuffle

import fnv
from utils import timeit, get_qid_question, jaccard_sim, make_dict


p = 15373875993579943603
x = 0.6
s = 14
r = 6
ult_minhash = {}
questions = {}


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


@timeit
def build_table(lines, U):
	global ult_minhash, questions

	# random number generation in lists length r
	A = [uuid.uuid4().int & (1<<64)-1 for i in range(r)]
	B = [uuid.uuid4().int & (1<<64)-1 for i in range(r)]
	
	# creating r permutation dicts 
	permutations = [{} for i in range(r)] 

	# hashing each word in ground set to create permutations, storing in dictionary
	for idx in range(r):
		a = A[idx]
		b = B[idx]

		# permute each word in the ground set
		for word in U:
			h = hash_function(a, b, word)
			permutations[idx][word] = h

	signatures = {}

	for line in lines[1:]:
		try:
			item_set = set()
			qid, question = get_qid_question(line)
			questions[qid] = question  # store original qid, question
			item_set.update(question.split())  # get unique words
			
			# compute minhash signature vector
			minhash_vect = [] 
			for i in permutations:
				minhash_vect.append(min([i[item] for item in item_set]))  
			
			# store minhash vector for qid for final similarity checking
			try:
				ult_minhash[qid].append(str(minhash_vect))
			except KeyError:
				ult_minhash[qid] = [str(minhash_vect)]

			# store qid at minhash signature for a single hash table (out of b tables)
			try:
				signatures[str(minhash_vect)].append(qid)
			except KeyError:
				signatures[str(minhash_vect)] = [qid]
		
		except ValueError:
			continue

	return signatures


def findsim(table, n):
	similar_qids = {}

	for qid in ult_minhash:
		similar_qids[qid] = ""
		signatures = ult_minhash[qid]
		common_set = set()

		# finding all qids with same minhash signature for final Jaccard sim check
		for sig, t in zip(signatures, table):
			qids_at_minhash = table[t][sig]
			common_set.update(qids_at_minhash)
		
		for qid2 in common_set:
			if qid == qid2:
				continue
			
			sim = jaccard_sim(questions[qid], questions[qid2])
			if sim >= x:
				similar_qids[qid] += str(qid2) if similar_qids[qid] == "" else "," + str(qid2)

	make_dict(similar_qids, n + "hash")


@timeit
def main(path, n):
	lines = [line.rstrip("\n")for line in open(path, encoding = "utf8")]
	U = ground_set(lines)

	# building s amount of tables, more redundancy = more accuracy
	D = {}
	for i in range(s):
		D[i] = build_table(lines, U)

	findsim(D, n)

if __name__ == "__main__":
	try:
		n = sys.argv[1]
	except IndexError:
		n = "150"
	fpath = "../data/question_{}k.tsv".format(n)

	main(fpath, n)
	
