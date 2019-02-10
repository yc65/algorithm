# -*- coding: utf-8 -*-
import codecs

# min_depth:  9
# max_depth:  19

def read_file(infile):
	data = []
	with codecs.open(infile, 'r', 'utf-8') as fi:
		f_data = fi.readlines()
	n = 0
	for line in f_data:
		if n != 0:
			data.append(int(line.strip()))
		n+=1
	return data

class MinHeap(object):
	"""docstring for MinHeap"""
	def __init__(self, arr_len):
		# arr_len is the number of vertices
		self.arr = [None]*(arr_len+1)
		self.count = 0
		self.min = None

	def extract_min(self):
		# print('extract min: ',  self.arr)
		res = self.min
		self.swap(1, self.count)
		self.arr[self.count] = None
		self.count -= 1 

		curr_id = 1
		lchild_id = curr_id*2
		rchild_id = curr_id*2+1

		while (lchild_id <= self.count and self.arr[curr_id].val>self.arr[lchild_id].val) or \
			(rchild_id<=self.count and self.arr[curr_id].val>self.arr[rchild_id].val):
			if lchild_id <= self.count and rchild_id<=self.count:
				if self.arr[lchild_id].val<self.arr[rchild_id].val:
					self.swap(curr_id, lchild_id)
					curr_id = lchild_id
				else:
					self.swap(curr_id, rchild_id)
					curr_id = rchild_id
			elif lchild_id <= self.count:
				self.swap(curr_id, lchild_id)
				curr_id = lchild_id				
			else:
				self.swap(curr_id, rchild_id)
				curr_id = rchild_id				

			lchild_id = curr_id*2
			rchild_id = curr_id*2+1
		self.min = self.arr[1]
		return res

	def insert(self, x):
		# print("insert a node", x.val)
		self.count += 1
		self.arr[self.count] = x
		curr_id = self.count
		parent_id = int(self.count/2)
		while curr_id > 1 and self.arr[curr_id].val < self.arr[parent_id].val:
			self.swap(curr_id, parent_id)
			curr_id = parent_id
			parent_id = int(curr_id/2)
		self.min = self.arr[1]

	def swap(self, a, b):
		self.arr[a], self.arr[b] = self.arr[b], self.arr[a]
		
class Node(object):
	"""docstring for Node"""
	def __init__(self, val):
		self.val = val
		self.lchild = None
		self.rchild = None

def huffman_code(h_arr):
	min_heap = MinHeap(len(h_arr))
	root = None
	for x in h_arr:
		x_node = Node(x)
		min_heap.insert(x_node)

	while min_heap.count > 1:
		min_a = min_heap.extract_min()
		min_b = min_heap.extract_min()
		ab = Node(min_a.val+min_b.val)
		ab.lchild = min_b
		ab.rchild = min_a
		min_heap.insert(ab)
		if min_heap.count == 1:
			root = ab

	return root

def min_depth(root):
	if root == None:
		return 0

	if root.lchild == None and root.rchild == None:
		return 1

	if root.lchild == None:
		return min_depth(root.rchild)

	if root.rchild == None:
		return min_depth(root.lchild)

	return min(min_depth(root.rchild), min_depth(root.lchild)) + 1

def max_depth(root):
	if root == None:
		return 0

	return max(max_depth(root.lchild), max_depth(root.rchild))+1

def dfs(root):
	print("dfs loop: ", root.val)
	if root.lchild != None:
		dfs(root.lchild)
	if root.rchild != None:
		dfs(root.rchild)


if __name__ == '__main__':
	from sys import argv
	infile = argv[1]
	data = read_file(infile)
	root = huffman_code(data)
	# dfs(root)
	print('min_depth: ', min_depth(root)-1)
	print('max_depth: ', max_depth(root)-1)




		