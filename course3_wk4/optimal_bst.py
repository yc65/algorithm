# -*- coding:utf-8 -*-

def construct_optimal_bst(arr):
	arr_len = len(arr)
	cache = [[0]*(arr_len+1) for i in range(arr_len+1)]
	s = 0
	for s in range(arr_len):
		for i in range(1, arr_len+1):
			j = i+s
			if j<arr_len+1:
				# print("i: ", i, "j: ", j)
				part_a = 0
				part_b = []
				part_c = []
				for r in range(i,j+1):
					# print('r: ', r)
					part_a += arr[r-1]
					# print (cac he)
					if r-1>=i:
						part_b.append(cache[i][r-1])
					else:
						part_b.append(0)
					if r+1<=j:
						part_c.append(cache[r+1][j])
					else:
						part_c.append(0)
				assert len(part_b) == len(part_c)

				candidates_num = len(part_b)
				the_min = 10000
				for x in range(candidates_num):
					temp = part_b[x] + part_c[x] + part_a
					# print ("temp:  ", temp)
					if temp < the_min:
						the_min = temp
				assert the_min != 10000
				# print("the_min: ", the_min)
				# print("i:  ", i, "j:  ", j)
				cache[i][j] = the_min
	return cache


if __name__ == '__main__':
	arr = [0.2, 0.05, 0.17, 0.10, 0.20, 0.03, 0.25]
	res = construct_optimal_bst(arr)
	print(res[1][7])
