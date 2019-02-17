#!/usr/bin/python3


class KaratsubaMult:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def split_num(self, num):
		a = ""
		b = ""
		count = 0
		mid = 0
		if len(num)%2 == 0:
			mid = int(len(num)/2)
		else:
			mid = int((len(num)+1)/2)

		for i in range(mid):
			a += num[i]
		for i in range(mid, len(num)):
			b += num[i]

		return a, b

	def char_add(self, x, y):
		# print ("x: ", x, "y: ", y)
		len_x = len(x)
		len_y = len(y)
		lenth = 0
		sum_char = []
		add_one = False


		if len_x > len_y:
			lenth = len_x
		else:
			lenth = len_y
		for i in range(lenth):
			i_x = len_x-i-1
			if i_x >= 0:
				x_single = int(x[i_x])
			else:
				x_single = 0
			i_y = len_y-i-1
			if i_y >=0:
				y_single = int(y[i_y])
			else:
				y_single = 0
			sum_single = x_single+y_single

			if add_one == True:
				sum_single += 1

			if sum_single > 9 and sum_single < 20:
				sum_char.insert(0, str(sum_single-10))
				add_one = True
			elif sum_single <=9:
				sum_char.insert(0, str(sum_single))
				add_one = False
			else:
				print("warning sum_single exceeds 19 \n")

		if add_one == True:
			sum_char.insert(0, str(1))

		return "".join(sum_char)

	def char_substract(self, x, y):
		len_x = len(x)
		len_y = len(y)
		substract_one = False
		substract_char = []
		if len_x<len_y:
			print("WARNING: x is larger than one - not supported for substraction")
		else:
			count = len_x
			for i in range(count):
				i_x = len_x - i - 1
				if i_x>=0:
					x_single = int(x[i_x])
				else:
					x_single = 0

				i_y = len_y-i-1
				if i_y >=0:
					y_single = int(y[i_y])
				else:
					y_single = 0

				if substract_one == True:
					x_single-=1

				if x_single>=y_single:
					substract_char.insert(0,str(x_single-y_single))
					substract_one = False
				else:
					substract_char.insert(0, str(x_single+10-y_single))
					substract_one = True

		return "".join(substract_char)

	def append_zeros(self, num, len_zeros):
		for i in range(len_zeros):
			num+='0'
		return num


	def kara_recursion(self, x, y):
		len_x = len(x)
		len_y = len(y)
		res = 0

		if len_x == 1 or len_y == 1:
			res = str(int(x) * int(y))

		else:
			a, b = self.split_num(x)
			c, d = self.split_num(y)

			step1 = self.kara_recursion(a, c)
			# print("step1", step1)
			step2 = self.kara_recursion(b, d)
			# print("step2", step2)
			a_plus_b = self.char_add(a, b)
			c_plus_d = self.char_add(c, d)
			step3 = self.kara_recursion(a_plus_b, c_plus_d)
			# print ("step3",step3)

			subs32 = self.char_substract(step3, step2)
			# print("subs32", subs32)
			subs321 = self.char_substract(subs32, step1)
			# print("subs321", subs321)

			b_plus_d_len = len(b)+len(d)
			bd_max_len = max(len(b), len(d))

			step1_pad = self.append_zeros(step1, b_plus_d_len)
			subs321_pad = self.append_zeros(subs321, bd_max_len)

			sum_res1 = self.char_add(step1_pad, step2)
			# print("sum_res1", sum_res1)
			res = self.char_add(sum_res1, subs321_pad)
			# print("res", res)

		return res

	def run(self):
		res = self.kara_recursion(self.x, self.y)
		print(res)

if __name__ == "__main__":
	A = "3141592653589793238462643383279502884197169399375105820974944592"
	B = "2718281828459045235360287471352662497757247093699959574966967627"

	tempa = "999910"
	tempb = "888801"

	kara = KaratsubaMult(A, B)
	kara.run()
	# print(kara.char_add("614", "190"))












