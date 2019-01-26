# -*- coding: utf-8 -*-
import codecs
import math

# for Q1: 69119377652
# for Q2: 67311454237

def read_file(infile):
	data = []
	with codecs.open(infile, 'r', 'utf-8') as fi:
		fdata = fi.readlines()
	n = 0
	for line in fdata:
		if n!=0:
			line = line.strip()
			weight, length = line.split(" ")
			data.append((int(weight), int(length)))
		n+=1

	return data

def calc_score_1(weight, length):
	return weight-length

def calc_score_2(weight, length):
	return weight/length

# arr in the form of [(weight, length), ...]
def merge(arr, arr_temp, left, mid, right):
	i = left
	j = mid+1
	k = left
	while i<=mid and j<=right:
		if calc_score_2(arr[i][0], arr[i][1]) < calc_score_2(arr[j][0], arr[j][1]):
			arr_temp[k] = arr[j]
			j+=1
			k+=1
		elif calc_score_2(arr[i][0], arr[i][1]) > calc_score_2(arr[j][0], arr[j][1]):
			arr_temp[k] = arr[i]
			i+=1
			k+=1
		else:
			if arr[i][0] < arr[j][0]:
				arr_temp[k] = arr[j]
				j+=1
				k+=1
			else:
				arr_temp[k] = arr[i]
				i+=1
				k+=1

	while i<= mid:
		arr_temp[k] = arr[i]
		k+=1
		i+=1

	while j<=right:
		arr_temp[k] = arr[j]
		j+=1
		k+=1

	for idx in range(left, right+1):
		arr[idx] = arr_temp[idx]


def merge_sort(arr, arr_temp, left, right):
	if left < right:
		mid = math.floor((left+right)/2)
		# print("mid is: ", mid)
		merge_sort(arr, arr_temp, left, mid)
		merge_sort(arr, arr_temp, mid+1, right)
		merge(arr, arr_temp, left, mid, right)


def calc_time(data):
	n = 0 
	num_data = len(data)

	data_temp = [(0, 0)]*num_data
	merge_sort(data, data_temp, 0, num_data-1)

	res = 0
	time = 0
	for job in data:
		time += job[1]
		res += job[0] * time

	return res

if __name__ == '__main__':
	from sys import argv
	infile = argv[1]
	data = read_file(infile)
	res = calc_time(data)
	print ("res is: ", res)







