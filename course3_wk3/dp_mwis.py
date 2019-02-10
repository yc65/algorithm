# -*-coding:utf-8 -*-

import codecs

# 10100110

def read_file(infile):
	n = 0
	data = []
	with codecs.open(infile, 'r', 'utf-8') as fi:
		fdata = fi.readlines()
	for line in fdata:
		if n == 0:
			data.append(-1)
		else:
			data.append(int(line.strip()))
		n+=1
	return data

def mwis(arr):
	dp_cache = []

	# initialize the first two of the dp_cache
	dp_cache.append(0)
	dp_cache.append(arr[1])

	# compute the dp_cache
	n = 2
	while n < len(arr):
		# print("n: ", n, "dp_cache: ", dp_cache)
		dp_cache.append(max(dp_cache[n-1], (dp_cache[n-2]+arr[n]))) 
		n += 1

	# reconstruct to get the set:
	res_mwis = []
	n = len(arr)-1
	while n>1:
		if (dp_cache[n-2]+arr[n])>dp_cache[n-1]:
			res_mwis.append(n)
			n -= 2
		else:
			n -= 1
	if n == 1:
		res_mwis.append(n)

	# test if vertices 1, 2, 3, 4, 17, 117, 517, and 997 are in the is:
	res_cache = [0]*8
	TEST_V = [1, 2, 3, 4, 17, 117, 517, 997]
	n = 0
	while n < 8:
		if TEST_V[n] in res_mwis:
			res_cache[n] = 1
		n += 1
	return ''.join([str(i) for i in res_cache])

if __name__ == '__main__':
	from sys import argv
	infile = argv[1]
	data = read_file(infile)
	res = mwis(data)
	print("the mwis is: ", res)


