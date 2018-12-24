# -*- coding: utf-8 -*-
import codecs
import math
# count inversions

def readfile(infile):
	data_int = []
	with codecs.open(infile) as fi:
		data = fi.readlines()
	for line in data:
		data_int.append(int(line.strip()))
	return data_int

def sort_and_count(arr, arr_temp, left, right):
	count_inv = 0
	if left<right:
		mid = math.floor((left+right)/2)
		count_inv += sort_and_count(arr, arr_temp, left, mid)
		count_inv += sort_and_count(arr, arr_temp, mid+1, right)
		count_inv += merge_and_count_split_inv(arr, arr_temp, left, mid, right)

	return count_inv

def merge_and_count_split_inv(arr, arr_temp, left, mid, right):
	i=left
	j = mid+1
	k = left
	count_inv = 0

	while i<=mid and j <=right:
		if arr[i] < arr[j]:
			arr_temp[k] = arr[i]
			i+=1
			k+=1
		else:
			arr_temp[k] = arr[j]
			count_inv += mid-i+1
			j+=1
			k+=1

	while i<=mid:
		arr_temp[k] = arr[i]
		i+=1
		k+=1

	while j<=right:
		arr_temp[k] = arr[j]
		j+=1
		k+=1

	for idx in range(left, right+1):
		arr[idx] = arr_temp[idx]

	return count_inv

def count_inv_main(infile):
	arr = readfile(infile)
	# arr = [1, 3, 7, 9, 5, 2, 4, 6]
	arr_temp = [0]*len(arr)
	count_inv = sort_and_count(arr, arr_temp, 0, len(arr)-1)

	return count_inv

if __name__ == '__main__':
	from sys import argv
	fi = argv[1]
	count_inv = count_inv_main(fi)
	print (count_inv)
