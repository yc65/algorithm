# -*- coding: utf-8 -*-

import codecs

def read_data(infile):
	data_int = []
	with codecs.open(infile) as fi:
		data = fi.readlines()

	for line in data:
		data_int.append(int(line.strip()))

	return data_int


class QuickSort(object):
	"""docstring for QuickSort"""
	def __init__(self, arr):
		self.arr = arr
		self.count = 0

	def pick_pivot_method_a(self, left, right):
		# choose the first element as the pivot
		return left, self.arr[left]

	def pick_pivot_method_b(self, left, right):
		return right, self.arr[right]

	def pick_pivot_method_c(self, left, right):
		candidates = []
		if (right-left+1)%2 == 0:
			candidates.append((left, self.arr[left]))
			candidates.append((int(left+(right-left-1)/2), self.arr[int(left+(right-left-1)/2)]))
			candidates.append((right, self.arr[right]))

		else:
			candidates.append((left, self.arr[left]))
			candidates.append((int(left+(right-left)/2), self.arr[int(left+(right-left)/2)]))
			candidates.append((right, self.arr[right]))
		candidates.sort(key=lambda x: x[1])
		# print ("candidates: ",candidates)
		mid = candidates[1]
		# print("left: ", self.arr[left], "right: ", self.arr[right], "mid: ", mid[1])
		assert self.arr[mid[0]] == mid[1]
		return mid[0], mid[1]

	def swap(self, i_x, i_y):
		temp = self.arr[i_x]
		self.arr[i_x] = self.arr[i_y]
		self.arr[i_y] = temp

	def quick_sort(self, left, right):
		# print ("left: ", left, "right: ", right)
		if left<right:
			# print ("before: ", self.arr)
			self.count += right-left
			# i_pivot, pivot = self.pick_pivot_method_a(left, right)
			i_pivot, pivot = self.pick_pivot_method_b(left, right)
			# i_pivot, pivot = self.pick_pivot_method_c(left, right)
			# print ("pivot: ", pivot)
			self.swap(left, i_pivot)

			#partition
			i = left+1
			j = left+1

			while (j<=right):
				if self.arr[j]>pivot:
					j+=1
				else:
					self.swap(i, j)
					i+=1
					j+=1

			self.swap(left, i-1)
			# print ("after: ", self.arr)
			self.quick_sort(left, i-2)
			self.quick_sort(i, right)
			
		return self.count

	def run(self):
		l = 0
		r = len(self.arr)-1
		self.quick_sort(l, r)

def veryfy(arr):
	for i in range(len(arr)-1):
		if arr[i+1]-arr[i] != 1:
			print("WARNING: ", arr[i+1], arr[i])


if __name__ == '__main__':
	from sys import argv
	import random
	fi = argv[1]
	arr = read_data(fi)

	# arr = []
	# for i in range(20):
	# 	arr.append(i)
	# random.seed(1)
	# random.shuffle(arr)

	# arr = [3,8,2,5,1,4,7,6]
	QS = QuickSort(arr)
	QS.run()
	# print (QS.arr)
	print (QS.count)
	veryfy(QS.arr)
