f = "question_10k.tsv"

lines=[line.rstrip("\n")for line in open(f, encoding = "utf8")]

#print(lines[2])

for line in lines[1:]:
	try:
		qid, question = line.split("\t")
		for word in question.split():
			if word == "Quora":
				print(question)
		#print(question)
	except ValueError:
		continue
