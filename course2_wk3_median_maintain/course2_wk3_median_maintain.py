# -*- coding: utf-8 -*-
import codecs

def read_file(fi):
	arr = []
	with codecs.open(fi, 'r', 'utf-8') as file_in:
		data = file_in.readlines()
	for line in data:
		line = line.strip()
		arr.append(int(line))
	return arr

class MinHeap(object):
	"""docstring for MinHeap"""
	def __init__(self):
		self.min_heap = [0]*10000
		self.num = 0
		self.min = 0

	def insert(self, x):
		self.num += 1
		self.min_heap[self.num]=x
		curr_id = self.num
		parent_id = int(curr_id/2)
		while self.min_heap[curr_id] < self.min_heap[parent_id] and curr_id >1:
			self.swap(curr_id, parent_id)
			curr_id = parent_id
			parent_id = int(curr_id/2)
		self.min = self.min_heap[1]

	def extract_min(self):
		res = self.min_heap[1]
		self.swap(1, self.num)
		self.min_heap[self.num] = 0
		self.num-=1

		curr_id = 1
		lchild_id = curr_id*2
		rchild_id = curr_id*2+1
		while (lchild_id<=self.num and self.min_heap[curr_id]>self.min_heap[lchild_id]) or \
			(rchild_id<=self.num and self.min_heap[curr_id]>self.min_heap[rchild_id]):
			if rchild_id <= self.num:	
				if self.min_heap[lchild_id]<self.min_heap[rchild_id]:
					self.swap(curr_id, lchild_id)
					curr_id = lchild_id
				else:
					self.swap(curr_id, rchild_id)
					curr_id = rchild_id
			else:
				self.swap(curr_id, lchild_id)
				curr_id = lchild_id
			lchild_id = curr_id*2
			rchild_id = curr_id*2+1
		self.min = self.min_heap[1]	
		return res		

	def swap(self, i, j):
		self.min_heap[i], self.min_heap[j] = self.min_heap[j], self.min_heap[i]

class MaxHeap(object):
	"""docstring for MaxHeap"""
	def __init__(self):
		self.max_heap = [0]*10000
		self.num = 0
		if self.num > 0:
			self.max = self.max_heap[1]
		else:
			self.max = 0

	def insert(self, x):
		self.num += 1
		self.max_heap[self.num]=x
		curr_id = self.num
		parent_id = int(curr_id/2)

		while self.max_heap[curr_id]>self.max_heap[parent_id] and curr_id >1:
			self.swap(curr_id, parent_id)
			curr_id = parent_id
			parent_id = int(curr_id/2)
		self.max = self.max_heap[1]

	def extract_max(self):
		res = self.max_heap[1]
		self.swap(1, self.num)
		self.max_heap[self.num] = 0
		self.num-=1

		curr_id = 1
		lchild_id = curr_id*2
		rchild_id = curr_id*2+1
		while (lchild_id<=self.num and self.max_heap[curr_id]<self.max_heap[lchild_id]) or \
			(rchild_id<=self.num and self.max_heap[curr_id]<self.max_heap[rchild_id]):
			if rchild_id<=self.num:
				if self.max_heap[lchild_id]> self.max_heap[rchild_id]:
					self.swap(curr_id, lchild_id)
					curr_id = lchild_id
				else:
					self.swap(curr_id, rchild_id)
					curr_id = rchild_id
			else:
				self.swap(curr_id, lchild_id)
				curr_id = lchild_id
			lchild_id = curr_id*2
			rchild_id = curr_id*2+1
		self.max = self.max_heap[1]
		return res

	def swap(self, i, j):
		self.max_heap[i], self.max_heap[j] = self.max_heap[j], self.max_heap[i]

def median_maintain(arr):
	medians = []
	max_heap = MaxHeap()
	min_heap = MinHeap()

	for i in range(len(arr)):
		md = 0
		x = arr[i]
		if x <= max_heap.max:
			max_heap.insert(x)
		else:
			min_heap.insert(x)

		assert (abs(max_heap.num - min_heap.num) <= 2)
		# balance the min_heap and the max_heap
		if max_heap.num - min_heap.num == 2:
			temp = max_heap.extract_max()
			min_heap.insert(temp)
		elif min_heap.num - max_heap.num == 2:
			temp = min_heap.extract_min()
			max_heap.insert(temp)

		# get the median
		if max_heap.num == min_heap.num:
			md = max_heap.max
		elif max_heap.num - min_heap.num == 1:
			md = max_heap.max
		elif min_heap.num - max_heap.num == 1:
			md = min_heap.min

		if md != 0:
			medians.append(md)
		else:
			# pass
			print("WARNING: not getting the median")
	print ("num medians: ", len(medians))
	assert(len(medians) == len(arr))
	mod = sum(medians)%10000
	print (medians)
	print (mod)

if __name__ == '__main__':
	from sys import argv
	fi = "Median.txt"
	arr = read_file(fi)
	median_maintain(arr)