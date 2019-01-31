# -*- coding: utf-8 -*-

import codecs
import math

# 106

def read_file(infile):
	data = []
	with codecs.open(infile, 'r', 'utf-8') as fi:
		line = fi.readline()
		num_vertex = int(line.strip())
		line = fi.readline()
		while line:
			entry = line.strip().split(' ')
			# (weight, vertex_a, vertex_b)
			data.append((int(entry[2]), int(entry[0]), int(entry[1]))) 
			line = fi.readline()
	print ("test: first five of the (unsorted) dataset", data[:5])
	return data, num_vertex

class Union(object):
	"""docstring for Union"""
	def __init__(self, arr, num_vertex):
		self.arr = arr
		self.arr_len = num_vertex
		self.roots = [0]*(self.arr_len+1) # 1 ~ n 
		self.rank = [0]*(self.arr_len+1)

	def initialize_union(self):
		for i in range(self.arr_len+1):
			self.roots[i] = i

	# use union by rank
	def union(self, root_a, root_b):
		if root_a == root_b:
			print("ERROR: cannot union the same root")
			return -1
		if self.rank[root_a] == self.rank[root_b]:
			self.roots[root_a] = root_b
			self.rank[root_b] += 1

		elif self.rank[root_a] > self.rank[root_b]:
			self.roots[root_b] = root_a

		else:
			self.roots[root_a] = root_b

	#u use path compression
	def find(self, x):
		if self.roots[x] == x:
			return x
		else:
			self.roots[x] = self.find(self.roots[x])
			# don't forget to return!!
			return self.roots[x]


# sort the edges by distance from smallest to the biggest
class MergeSort(object):
	"""docstring for MergeSort"""
	def __init__(self, arr):
		self.arr = arr
		self.arr_temp = [(0, 0, 0)]*len(arr)
		
	def merge(self, left, mid, right):
		i = left
		j = mid+1
		k = left

		while i <= mid and j <= right:
			if self.arr[i][0] < self.arr[j][0]:
				self.arr_temp[k] = self.arr[i]
				i += 1
				k += 1
			else:
				self.arr_temp[k] = self.arr[j]
				j += 1
				k += 1

		while i <= mid:
			self.arr_temp[k] = self.arr[i]
			i += 1
			k += 1
		
		while j <= right:
			self.arr_temp[k] = self.arr[j]
			j += 1
			k += 1

		for i in range(left, right + 1):
			self.arr[i] = self.arr_temp[i]

	def sort(self, left, right):
		if left < right:
			mid = int((left+right)/2)
			self.sort(left, mid)
			self.sort(mid+1, right)
			self.merge(left, mid, right)

# the main function for clustering
def clustering(arr, num_vertex, k=4):
	# sort the edges:
	MS = MergeSort(arr)
	MS.sort(0, len(arr)-1)
	arr = MS.arr
	print("sorted: ",arr)

	# union
	Unn = Union(arr, num_vertex)
	Unn.initialize_union()

	cluster_num = Unn.arr_len
	spacing = 0

	n = 0
	while cluster_num >= k and n < len(arr):
		edge = arr[n]
		weight, vertex_a, vertex_b = edge
		Unn.find(vertex_a)
		root_a = Unn.roots[vertex_a]
		Unn.find(vertex_b)
		root_b = Unn.roots[vertex_b]
		if root_a != root_b:
			Unn.union(root_a, root_b)
			cluster_num -= 1
			spacing = weight
		n += 1

	print (Unn.roots)
	print ("spacing: ", spacing)
	return spacing

if __name__ == '__main__':
	from sys import argv
	infile = argv[1]
	arr, num_vertex = read_file(infile)
	spacing = clustering(arr, num_vertex)








