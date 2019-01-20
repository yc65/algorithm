# -*- coding: utf-8 -*-

import codecs
import datetime

# time total:  1:15:51.303844
# 427

def read_data(infile):
	data = [] 
	with codecs.open(infile, 'r', 'utf-8') as fi:
		fi_data = fi.readlines()
	for line in fi_data:
		data.append(int(line.strip()))

	return data

def two_sums(arr):
	start_time = datetime.datetime.now()
	print ("start: ", start_time)
	hash_tab = {}
	res = 0
	# create the hash table
	t_init = -10000
	for i, x in enumerate(arr):
		y = t_init-x
		hash_tab[y] = i 
	for t in range(-10000, 10001):
		print ("processing for target: ", t)
		print (datetime.datetime.now())
		offset = t - t_init
		# print (offset)
		for x in arr:
			y = t - x
			if x-offset in hash_tab and x != y:
				res += 1
				break
	end_time = datetime.datetime.now()
	print ("time total: ", end_time-start_time)
	return res

if __name__ == '__main__':
	from sys import argv
	f = argv[1]
	data = read_data(f)
	res = two_sums(data)
	print(res)