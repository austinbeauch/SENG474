from fnv import *
import uuid
import numpy
import re


p =  15373875993579943603
def testing(f):

	lines = [line.rstrip("\n")for line in open(f, encoding = "utf8")]
	m = 1
	for line in lines[1:]:
		try:
			qid, question = line.split("\t")
			question = re.sub(r'[^a-zA-Z0-9 ]+', r'', question)
			question = question.lower()
			for word in question.split():
				# word = word.encode("utf-8")
				hashcode = hash(word.encode("utf-8"), bits=64)
				
				for i in range(0, 14):
					k = hash_function(a[i], b[i], hashcode)
					if k in B[i]:
						B[i][k].append(qid)	
					else:
						B[i][k] = [qid, word]	
				#if word == "Quora":
					#print(type(question))
					#question = question.encode("utf-8")
					#hashcode = hash(question, bits=64) # fnv.fnv_1a is a default algorithm
					#print(hashcode)
			#print(question)
		except ValueError:
			continue
	return m

def hash_function(a,b,fnvh):
	hf = (a*fnvh + b)% p
	return(hf)

if __name__ == "__main__":
	n = "4"
	fpath = "../data/question_{}k.tsv".format(n)
	#data = pd.read_table(fpath, index_col=0)
	a = [uuid.uuid4().int & (1<<64)-1 for i in range(0,14)]
	b = [uuid.uuid4().int & (1<<64)-1 for i in range(0,14)]
	#print(a)
	#print(b)
	rand64 = uuid.uuid4().int & (1<<64)-1
	#print("a = 2, b = 3, fnvh = 10")
	#print(hash_function(a[0],b[0],100))
	
	B = [{} for i in range(0,14)]
	#for i in range(0,14):
	#B[2][2] = ["Hello World"]
	#print(B[2])
	#B[2][2].append("wee")
	#print(B[2])
	m = testing(fpath)
	#print(B[1].keys())
	print(min(B[1].keys()))
	print(B[1][min(B[1].keys())])
	print("What")
	print(m in B[1].keys())
