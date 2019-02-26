from pprint import pprint
s = 5

D = {}
FI = {}
def findFactors(num):
	l = []
	for i in range(1,num+1):
		if num % i == 0:
			l.append(i)
			
	return l

for i in range(1,101):
	D[i] = findFactors(i)
	for j in range(1,101):
		FI[str([i,j])] = 0
	

#pprint(D)

for i in D:
	for j in D[i]:
		for k in D[i]:
			if(j != k):
				FI[str([j,k])] = FI[str([j,k])] + 1
		
for i in FI:
	if FI[i] >= s:
		print(i)

