# -*- coding: utf-8 -*-
import codecs
import random

def get_data(infile):
	all_data = []
	with codecs.open(infile) as fi:
		data = fi.readlines()
	fi.close()

	for line in data:
		all_data.append(line.strip().split('	'))

	return all_data

class AdjNode(object):
	"""docstring for AdjNode"""
	def __init__(self, data):
		self.vertex = data
		self.next = None

class Graph(object):
	"""docstring for Graph"""
	def __init__(self, data):
		self.data = data
		self.V_num = len(data)
		# self.graph = [None]*(self.V_num+1)
		# vertex index starts from 1, thus below
		self.graph = dict.fromkeys(list(range(1, self.V_num+1)))
	
	def add_adge(self, src, dest):
		# print("add_adge ", dest, "to", src)
		new_node = AdjNode(dest)
		new_node.next = self.graph[src]
		self.graph[src] = new_node

		# below are not used since the both directions have been recorded in the input file
		# new_node = AdjNode(src)
		# new_node.next = self.graph[dest]
		# self.graph[dest] = new_node

	def remove_adge(self, src, dest_list):
		# print("remove_adge ", self.graph[src].vertex)
		n = 0
		curr_node = self.graph[src]
		# deal with dest in the beginning of the linked list
		# print("curr_node first: ", curr_node.vertex)
		while curr_node and curr_node.vertex in dest_list:
			curr_node = curr_node.next
			self.graph[src] = curr_node
			# print("curr_node begin: ", curr_node.vertex)

		# note the first node in the linked list won't be in the dest_list anymore,
		# so we loop from the second node
		if curr_node:
			prev_node = curr_node
			curr_node = curr_node.next
		
			while curr_node:
				if curr_node.vertex in dest_list :
					curr_node = curr_node.next
					prev_node.next = curr_node
				else:
					prev_node = curr_node
					curr_node = curr_node.next

	def create_graph(self):
		# print(self.data)
		for entry in self.data:
			src =int(entry[0])
			for dst in entry[1:]:
				# print("src: ", src, "dest: ", dst)
				self.add_adge(src, int(dst))

	def print_graph(self):
		for i in range(1, self.V_num+1):
			tempt = self.graph[i]
			print(i)
			while tempt:
				print("->",tempt.vertex)
				tempt = tempt.next
			print("\n")

class MinCut(object):
	"""docstring for MinCut"""
	def __init__(self, graph):
		self.graph = graph
		
	def contract(self, i, j):
		# merge i into j
		remaining_dest = []
		node_i = self.graph.graph[i]
		while node_i:
			remaining_dest.append(node_i.vertex)
			node_i = node_i.next
		self.graph.graph[i] = None

		node_j = self.graph.graph[j]
		for idx in remaining_dest:
			self.graph.add_adge(j, idx)
			if self.graph.graph[idx]:
				self.graph.add_adge(idx, j)
				self.graph.remove_adge(idx, [i])

	def contract_w_random(self, i):
		# merge i into j where j is randomly choosen from graph[i]
		remaining_dest = []
		node_i = self.graph.graph[i]
		while node_i:
			remaining_dest.append(node_i.vertex)
			node_i = node_i.next
		self.graph.graph[i] = None

		j = random.choice(remaining_dest)
		node_j = self.graph.graph[j]
		for idx in remaining_dest:
			self.graph.add_adge(j, idx)
			self.graph.remove_adge(j, [j])
			if self.graph.graph[idx]:
				self.graph.add_adge(idx, j)
				self.graph.remove_adge(idx, [i,idx])

		return j

	def find_min_cut(self):
		print("\nenter find_min_cut")
		n = self.graph.V_num
		all_vertices = list(range(1, n+1))
		# random.seed(1)
		random.shuffle(all_vertices)

		while n>2:
			merge_from = all_vertices.pop()
			# print("merge from: ", merge_from)
			merge_to = self.contract_w_random(merge_from)
			# print("merge ", merge_from, "to", merge_to)
			n-=1

		node_a = self.graph.graph[all_vertices[0]]
		node_b = self.graph.graph[all_vertices[1]]
		assert node_a != None
		assert node_b != None

		num_dest_a = 0
		num_dest_b = 0

		while node_a:
			num_dest_a+=1
			node_a = node_a.next
		while node_b:
			num_dest_b+=1
			node_b = node_b.next

		print ("num_dest_a: ", num_dest_a, "num_dest_b: ", num_dest_b)
		# self.graph.print_graph()
		assert num_dest_b == num_dest_a

		return num_dest_a

if __name__ == '__main__':
	from sys import argv
	in_file = argv[1]
	data = get_data(in_file)
	# graph = Graph(data)
	# graph.create_graph()
	# print("before: ")
	# graph.print_graph()
	# graph.remove_adge(2, [3,4,5,1])
	# print("after: ")
	# graph.print_graph()
	# mincut = MinCut(graph)

	all_mincut = []
	for i in range(50):
		graph = Graph(data)
		graph.create_graph()
		mincut = MinCut(graph)
		result = mincut.find_min_cut()
		all_mincut.append(result)

	print("result: ", min(all_mincut))









