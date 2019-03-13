import numpy as np

def PageRank():
	M = np.matrix([[1/3.0, 1/2.0, 0], [1/3.0, 0, 1/2.0], [1/3.0, 1/2.0, 1/2.0]])
	v0 = np.array([1/3.0, 1/3.0, 1/3.0])
	B = 0.8

	deg_v = np.array([3,2,2])
	v = np.array([0.0,0.0,0.0])

	for T in range(0,75):
		for i in range(0,3):
			v[i] = 0.8*sum([v0[j]/deg_v[j] for j in range(0,3) if M[i,j] != 0 ]) +0.2/3
		v0 = v

	print(M)

	print(v)

def HubAuth():
	M = np.matrix([[0, 1/2.0, 1, 0], [1/3.0, 0, 0, 1/2.0], [1/3.0, 0, 0, 1/2.0], [1/3.0, 1/2.0, 0, 0]])
	a = np.array([1/2.0, 1/2.0, 1/2.0, 1/2.0])
	h = np.array([1/2.0, 1/2.0, 1/2.0, 1/2.0])
	a_temp = np.array([1/2.0, 1/2.0, 1/2.0, 1/2.0])
	h_temp = np.array([1/2.0, 1/2.0, 1/2.0, 1/2.0])
	
	for T in range(0,50):
		for i in range(0,4):
			h_temp[i] = sum([a[j] for j in range(0,4) if M[j,i] != 0])
			a_temp[i] = sum([h[j] for j in range(0,4) if M[i,j] != 0])
		a = a_temp/np.sqrt((a_temp**2).sum())
		h = h_temp/np.sqrt((h_temp**2).sum())
		#if T%5 == 0:
		#	print("Iteration ", T)
		#	print(a)
		#	print(h)
		
	print(a)
	print(h)

	
def main():
	PageRank()
	#HubAuth()

	
	
if __name__ == "__main__":
	main()