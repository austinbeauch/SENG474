import re
import time

# https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
def jaccard_sim(str1, str2): 
    a = set(str1.split()) 
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def get_qid_question(line):
	"""Return qid and question from tab separated line, filter out puncuation and lowercase all letters"""
	qid, question = line.split("\t")
	question = re.sub(r'[.,!?@#$%^&*():;"]+', r'', question)
	question = question.lower()
	return qid, question


def timeit(method):
	def timed(*args, **kw):
		ts = time.time()
		result = method(*args, **kw)
		te = time.time()
		print('%r  %2.2f s' % \
				(method.__name__, (te - ts)))
		return result
	return timed