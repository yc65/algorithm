# -*- coding: utf-8 -*-
import codecs
from collections import defaultdict

# -3612829

def read_file(infile): # and create the graph
	graph = defaultdict(dict)
	with codecs.open(infile, 'r', 'utf-8') as fi:
		f_data = fi.readlines()
	n = 0
	for line in f_data:
		if n != 0:
			line = line.strip()
			va, vb, weight = line.split(" ")
			graph[int(va)][int(vb)] = int(weight)
			graph[int(vb)][int(va)] = int(weight)
		n+=1

	# print(graph)
	return graph

def prim_mst(graph):
	X = [1]
	V = []
	non_X_num = 0
	cost = 0
	
	# fill the non_X
	for k, v in graph.items():
		V.append(k)
		if k != 1:
			non_X_num += 1

	# mst  - note: could be optimized with heap like dijkstra
	while non_X_num:
		min_weight = 1000000
		dst_v = 0
		for src in X:
			dsts = graph[src].keys()
			for d in dsts:
				w = graph[src][d]
				if w<min_weight and d not in X:
					min_weight = w
					dst_v = d 

		if dst_v != 0:
			X.append(dst_v)
			non_X_num -= 1
			cost += min_weight
		else:
			break

	assert( len(X) == len(V) )
	return cost

if __name__ == '__main__':
	from sys import argv
	infile = argv[1]
	graph = read_file(infile)
	cost = prim_mst(graph)
	print ("cost is: ", cost)




