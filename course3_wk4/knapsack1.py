# -*- coding: utf-8 -*-
import codecs
import time

# 2493893
# 4243395

def readfile(infile):
	values = [0]
	weights = [0]
	with codecs.open(infile, 'r', 'utf-8') as fi:
		fdata = fi.readline()
		capacity, items_num = fdata.strip().split(' ')
		fdata = fi.readline()

		while fdata:
			print("readdata....")
			v, w = fdata.strip().split(' ')
			weights.append(int(w))
			values.append(int(v))
			fdata = fi.readline()
	return int(capacity), int(items_num), values, weights

def knapsacks_dp(capacity, item_nums, values, weights):
	cache = [[0]*(capacity+1) for i in range(item_nums+1)]
	for i in range(1,item_nums+1):
		for w in range(1,capacity+1):
			choice_a = cache[i-1][w]
			if w-weights[i] >= 0:
				choice_b = cache[i-1][w-weights[i]] + values[i]
			else:
				choice_b = 0
			cache[i][w] = max(choice_a, choice_b)
	return cache

def knapsacks_dp_opt(capacity, item_nums, values, weights):
	cache = [[0] * (capacity+1) for i in range(2)]
	for i in range(1, item_nums+1):
		# if i % 100 == 0:
		print(i, time.time())
		cache[0] = cache[1]
		cache[1] = [0]*(capacity+1) # don't forget to reset!
		for w in range(1, capacity+1):
			choice_a = cache[0][w]
			if w-weights[i] >= 0:
				choice_b = cache[0][w-weights[i]] + values[i]
			else:
				choice_b = 0
			cache[1][w] = max(choice_a, choice_b)
	return cache

if __name__ == '__main__':
	from sys import argv
	infile = argv[1]
	capacity, item_nums, values, weights = readfile(infile)
	# cache = knapsacks_dp(capacity, item_nums, values, weights)
	# print (cache)
	# print(cache[item_nums][capacity])

	start = time.time()
	print("start: ", start)
	cache = knapsacks_dp_opt(capacity, item_nums, values, weights)
	end = time.time()
	print("end: ", end)
	# print (cache)
	print(cache[1][capacity])





