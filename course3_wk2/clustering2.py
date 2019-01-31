# -*- coding: utf-8 -*-
import codecs
from collections import defaultdict

# 6118

def bin_to_int(infile):
	number_dict = defaultdict(list) # the dictionary map number encoded by 1/0 to vertices
	with codecs.open(infile, 'r', 'utf-8') as fi:
		fdata = fi.readline()
		vertex_num = int(fdata.strip().split(' ')[0])
		fdata = fi.readline()
		n = 1
		while fdata:
			bin_num = ''.join(fdata.split(' '))
			int_num = int(bin_num,2)
			number_dict[int_num].append(n)
			n+=1
			fdata = fi.readline()

		return number_dict, vertex_num

class Union(object):
	"""docstring for Union"""
	def __init__(self, vertex_num):
		self.vertex_num = vertex_num
		self.roots = [0]*(vertex_num+1)
		self.ranks = [0]*(vertex_num+1)

	def init_union(self):
		for i in range(self.vertex_num+1):
			self.roots[i] = i

	def find(self, x):
		if self.roots[x] == x:
			return x
		else:
			self.roots[x] = self.find(self.roots[x])
			return self.roots[x]

	def union(self, root_x, root_y):
		if self.ranks[root_x] == self.ranks[root_y]:
			self.roots[root_x] = root_y
			self.ranks[root_y] += 1

		elif self.ranks[root_x] > self.ranks[root_y]:
			self.roots[root_y] = root_x

		else:
			self.roots[root_x] = root_y

def mask_len_1(num, len_bin_num=24):
	# use 1 to convert from zero to one or from one to zero
	complement_num = []
	masks = [1<<i for i in range(len_bin_num)]
	for m in masks:
		complement_num.append(num^m)
	return complement_num

def mask_len_2(num, len_bin_num=24):
	complement_num = []
	masks = [1<<i for i in range(len_bin_num)]
	n1 = 0
	while n1 < len_bin_num:
		m1 = masks[n1]
		n2 = n1+1
		while n2 < len_bin_num:
			if n2 != n1:
				m2 = masks[n2]
				num_temp = num^m1
				num_temp = num_temp^m2
				complement_num.append(num_temp)
			n2 += 1
		n1 += 1
	return complement_num

def get_neighbours(num):
	neighbours = mask_len_1(num)
	neighbours.extend(mask_len_2(num))
	return neighbours

def solution(number_dict, vertex_num):
	cluster = vertex_num
	U = Union(vertex_num)
	U.init_union()
	nums = number_dict.keys() # all numbers of the vertices
	for n in nums:
		vertices = number_dict[n]
		neighbours = get_neighbours(n)
		for nb in neighbours: 
			if nb in number_dict:
				vertices.extend(number_dict[nb])
		# union all vertices - randomly choose a root and union one by one
		assert len(vertices)>0
		vertex_a = vertices[0]
		for vertex_b in vertices[1:]:
			root_a = U.find(vertex_a)
			root_b = U.find(vertex_b)
			if root_a != root_b:
				U.union(root_a, root_b)
				vertex_a = vertex_b
				cluster -= 1
	return cluster



if __name__ == '__main__':
	# U = Union(200000)
	# import math
	# complement_num = mask_len_1(15, int(math.log(15, 2))+1)
	# print ([bin(n) for n in complement_num])
	# print ([n for n in complement_num])
	from sys import argv
	infile = argv[1]
	number_dict, vertex_num = bin_to_int(infile)
	cluster = solution(number_dict, vertex_num)
	print("result: ", cluster)











