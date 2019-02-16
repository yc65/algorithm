# -*- coding: utf-8 -*-

import codecs
from collections import defaultdict
import numpy as np

INFINIT = 1000000

# g1 None
# g2 None
# g3 -19

def read_file_and_create_graph(infile):
	graph = defaultdict(dict)
	graph_rev = defaultdict(dict)
	with codecs.open(infile, 'r', 'utf-8') as fi:
		fdata = fi.readline()
		stat = fdata.strip().split(' ')
		# print (stat)
		vertices_num, edge_num = int(stat[0]), int(stat[1])
		fdata = fi.readline()
		while fdata:
			edge = fdata.strip().split(' ')
			# print(edge)
			vertex_from = int(edge[0])
			vertex_to = int(edge[1])
			weight = int(edge[2])
			try:
				if graph[vertex_from][vertex_to] > weight:
					graph[vertex_from][vertex_to] = weight
			except:
				graph[vertex_from][vertex_to] = weight
			
			try:
				if graph_rev[vertex_to][vertex_from] > weight:
					graph_rev[vertex_to][vertex_from] = weight
			except:
				graph_rev[vertex_to][vertex_from] = weight
			fdata = fi.readline()

	return graph, graph_rev, vertices_num, edge_num


class MinHeap(object):
	"""docstring for MinHeap"""
	def __init__(self, vertices_num):
		self.heap = [None]*(vertices_num+1) # [(vertex, dijkstra_value,)..]
		self.map = {k:0 for k in range(vertices_num+1)} # NEED ONLY for dijkstra: map from vertex to the location in the heap
		self.num = 0
		self.vertices_num = vertices_num

	def swap(self, idx, idy):
		vertex_x = self.heap[idx][0]
		vertex_y = self.heap[idy][0]
		self.map[vertex_x] = idy
		self.map[vertex_y] = idx
		self.heap[idx], self.heap[idy] = self.heap[idy], self.heap[idx]


	def initialize(self, start, graph):
		dsts = graph[start]
		for d, weight in dsts.items():
			if d != start:
				self.insert((d, weight))

		n = 1
		for vertex in range(1, vertices_num+1):
			if vertex != start and self.map[vertex] == 0:
				self.insert((vertex, INFINIT))
				n += 1
		# print("heap in initialize: ", self.heap)
		# print("map in initialize: ", self.map)

	def insert(self, vertex_w_score):
		self.num += 1
		self.heap[self.num] = vertex_w_score
		self.map[vertex_w_score[0]] = self.num 
		curr_id = self.num
		parent_id = int(curr_id/2)
		while curr_id >1 and self.heap[parent_id][1] > self.heap[curr_id][1]:
			self.swap(parent_id, curr_id)
			curr_id = parent_id
			parent_id = int(curr_id/2)

	def delete(self, heap_id):
		self.map[self.heap[heap_id][0]] = 0
		self.swap(heap_id, self.num)
		self.heap[self.num] = None
		self.num -= 1
		curr_id = heap_id
		parent_id = int(heap_id/2)
		lchild_id = heap_id*2
		rchild_id = heap_id*2+1

		while curr_id > 1 and curr_id <=self.num:
			if self.heap[curr_id][1] < self.heap[parent_id][1]:
				self.swap(curr_id, parent_id)
				curr_id = parent_id
				parent_id = int(curr_id/2)
			else:
				break

		while (( lchild_id<=self.num and self.heap[lchild_id][1] < self.heap[curr_id][1]) or \
			(rchild_id<=self.num and self.heap[rchild_id][1] < self.heap[curr_id][1])):
			if rchild_id<=self.num:
				if self.heap[lchild_id][1] < self.heap[rchild_id][1]:
					self.swap(lchild_id, curr_id)
					curr_id = lchild_id
				else:
					self.swap(rchild_id, curr_id)
					curr_id = rchild_id
			else:
				self.swap(lchild_id, curr_id)
				curr_id = lchild_id
			lchild_id = curr_id * 2
			rchild_id = curr_id * 2 + 1

	def extract_min(self):
		# print("heap in extract_min: ", self.heap)
		# print("map in extract_min: ", self.map)
		the_min = self.heap[1]
		
		# swap the min with the last one
		self.swap(1, self.num)
		# delete the last one
		self.heap[self.num] = None
		self.num -= 1
		self.map[the_min[0]] = 0
		# adjust the heap
		curr_id = 1
		lchild_id = curr_id*2
		rchild_id = curr_id*2+1
		while (lchild_id<=self.num and self.heap[curr_id][1]>self.heap[lchild_id][1]) or \
			(rchild_id<=self.num and self.heap[curr_id][1]>self.heap[rchild_id][1]):
			if rchild_id <= self.num:	
				if self.heap[lchild_id][1]<self.heap[rchild_id][1]:
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

		return the_min # in the from of (vertex, dijkstra score)

	def update(self, vertex_extracted, graph):
		# print("update heap", self.heap, "\nafter extracting ", vertex_extracted[0])
		vertex, score = vertex_extracted
		dsts = graph[vertex]
		for d, w in dsts.items():
			if self.map[d] != 0:
				d_heap_id = self.map[d]
				# print("d_heap_id: ", d_heap_id, "d: ", d)
				dst_w_score = self.heap[d_heap_id]
				new_score = min(dst_w_score[1], score + w)
				# print("new_score", new_score)
				if new_score != dst_w_score[1]:
					self.delete(d_heap_id)
					self.insert((d, new_score))


def dijkstra(graph, vertices_num, start_v):
	shortest_path = [0]*(vertices_num+1)

	min_heap = MinHeap(vertices_num)
	min_heap.initialize(start_v, graph)
	while min_heap.num > 0:
		vertex, score = min_heap.extract_min()
		shortest_path[vertex] = score
		if min_heap.num != 0:
			min_heap.update((vertex, score), graph)
	
	return min(shortest_path), shortest_path

def bellman_ford(graph_rev, vertices_num, start_v):
	cache = [[INFINIT]*(vertices_num+1) for i in range(vertices_num+1)]
	cache[0][0] = 0
	for v in range(1, vertices_num+1):
		cache[1][v] = 0
		cache[0][v] = 0
		cache[v][0] = 0
	for i in range(1, vertices_num+1):
		for v in range(1, vertices_num+1):
			candidate_a = cache[i-1][v]
			candidata_b = INFINIT
			srcs = graph_rev[v]
			for s, w in srcs.items():
				if cache[i-1][s] + w < candidata_b:
					candidata_b = cache[i-1][s] + w 
			cache[i][v] = min(candidate_a, candidata_b)
	# test negative cycle:
	has_negative_cycle = False
	for vertex in range(vertices_num+1):
		if cache[vertices_num-1][vertex] != cache[vertices_num][vertex]:
			has_negative_cycle = True
	if has_negative_cycle:
		return None, None
	else:
		# print(cache)
		return min(cache[vertices_num]), cache[vertices_num]

def floyd_warshall(graph, vertices_num):
	cache = [[[0] * (vertices_num+1) for i in range(vertices_num+1)] for j in range(vertices_num+1)]
	# cache = np.zeros((vertices_num+1, vertices_num+1, vertices_num+1), dtype=int) # (k, i, j)

	# init the 3-d array
	for i in range(1, vertices_num+1):
		for j in range(1, vertices_num+1):
			print("i: ", i, "j: ", j)
			if i == j:
				for k in range(0, vertices_num+1):
					cache[k][i][j] = 0 
			elif i in graph.keys() and j in graph[i].keys():
				cache[0][i][j] = graph[i][j]
				for k in range(1, vertices_num+1):
					cache[k][i][j] = INFINIT
			else:
				for k in range(0, vertices_num+1):
					cache[k][i][j] = INFINIT
	
	# the dp
	the_min = INFINIT
	for k in range(1, vertices_num+1):
		for i in range(1, vertices_num+1):
			for j in range(1, vertices_num+1):
				candidate_a = cache[k-1][i][j]
				candidate_b = cache[k-1][i][k] + cache[k-1][k][j]
				cache_value = min(candidate_a, candidate_b)
				cache[k][i][j] = cache_value
				if k == vertices_num:
					if cache_value < the_min:
						the_min = cache_value

	# res
	print(cache)
	has_negative_path = False
	for k in range(1, vertices_num+1):
		for x in range(1, vertices_num+1):
			if cache[k][x][x] < 0:
				has_negative_path = True
	
	if has_negative_path == False:
		return the_min
	else:
		return None
 
def johnson(graph, graph_rev, vertices_num):
	# reweighting - add vertex 0
	print("reweighting - add vertex 0")
	for i in range(vertices_num+1):
		graph[0][i] = 0
		graph_rev[i][0] = 0
	
	# reweighting - generate weights of vertices
	print("reweighting - generate weights of vertices")
	res, weights = bellman_ford(graph_rev, vertices_num, 0)
	if res == None:
		return None

	# reweighting - reweights the edges in the graph
	print("reweighting - reweights the edges in the graph")
	for i in graph.keys():
		for j in graph[i]:
			graph[i][j] = graph[i][j]+weights[i]-weights[j]

	# run dijkstra for each vertex
	shortest_path = INFINIT
	src = 0
	dst = 0
	# shortest_paths = [0] * (vertices_num+1)
	for v in range(0, vertices_num+1):
		print("run dijkstra on v: ", v)
		_, dijkstra_shortest_paths = dijkstra(graph, vertices_num, v)
		n = 1
		while n < len(dijkstra_shortest_paths):
			# !!! notice: reversion of the reweighting needs to be done for every dst vertices from dijkstra
			# this is because some dst vertices may have the same dijkstra shortest path length,
			# but after the reversin the re-weighting, the final shortest path could be different
			dist = dijkstra_shortest_paths[n] + weights[n] - weights[v]
			if dist < shortest_path:
				shortest_path = dist
				dst = n
				src = v
			n+=1
	
	return shortest_path

if __name__ == '__main__':
	from sys import argv
	infile = "g3.txt"
	graph, graph_rev, vertices_num, edge_num = read_file_and_create_graph(infile)
	# print("graph: ", graph)
	# res, shortest_path = dijkstra(graph, vertices_num, 4)
	# print('4-16: ',shortest_path[16])
	
	# res, all_shortest_path = bellman_ford(graph_rev,vertices_num, 1)

	# res = floyd_warshall(graph, vertices_num)

	res = johnson(graph, graph_rev, vertices_num)
	print(res)
