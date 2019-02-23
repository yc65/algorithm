# -*- coding: utf-8 -*-
import codecs
from collections import defaultdict
import math

INFINITE = 10000000000

def readfile(infile):
    vertices = [(-1, -1)]
    with codecs.open(infile, 'r', 'utf-8') as fi:
        fdata = fi.readline()
        vertices_num = int(fdata.strip())
        fdata = fi.readline()
        while fdata:
            _, x, y = fdata.strip().split(' ')
            vertices.append((float(x), float(y)))
            fdata = fi.readline()
    return vertices, vertices_num



class MinHeap(object):
    """docstring for MinHeap"""
    def __init__(self, vertices_num):
        self.heap = [None]*(vertices_num+1) # [(vertex, min dist from X, src)..]
        self.map = {k:0 for k in range(vertices_num+1)} # NEED ONLY for dijkstra: map from vertex to the location in the heap
        self.num = 0
        self.vertices_num = vertices_num

    def swap(self, idx, idy):
        vertex_x = self.heap[idx][0]
        vertex_y = self.heap[idy][0]
        self.map[vertex_x] = idy
        self.map[vertex_y] = idx
        self.heap[idx], self.heap[idy] = self.heap[idy], self.heap[idx]


    def initialize(self, start, vertices):
        x1, y1 = vertices[1]
        for d in range(2, self.vertices_num+1):
            x2, y2 = vertices[d]
            self.insert((d, _distance(x1, y1, x2, y2), start))

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

    def update(self, vertex_extracted, vertices, X):
        # print("update heap", self.heap, "\nafter extracting ", vertex_extracted[0])
        vertex, _, src = vertex_extracted
        x1, y1 = vertices[vertex]
        for d in self.heap:
            if d != None and self.map[d[0]] != 0 :
                x2, y2 = vertices[d[0]]
                d_heap_id = self.map[d[0]]
                # print("d_heap_id: ", d_heap_id, "d: ", d)
                dst_w_score = self.heap[d_heap_id]
                new_score = min(dst_w_score[1], _distance(x1, y1, x2, y2))
                # print("new_score", new_score)
                if new_score != dst_w_score[1]:
                    self.delete(d_heap_id)
                    self.insert((d[0], new_score, vertex))


def _distance(x1, y1, x2, y2, sqrt=False):
    res = (x2-x1)**2+(y2-y1)**2
    if sqrt:
        res = math.sqrt(res)
    return res

def create_graph(vertices, vertices_num):
    graph = defaultdict(dict)
    for i in range(1, vertices_num+1):
        print("create graph for vertex: ", i)
        for j in range(i+1, vertices_num+1):
            x1, y1 = vertices[i]
            x2, y2 = vertices[j] 
            d = _distance(x1, y1, x2, y2)
            graph[i][j] = d
            graph[j][i] = d
    return graph

def mst_prim(vertices, vertices_num):
    X = [1]
    mst = defaultdict(list)
    V = [i for i in range(2, vertices_num+1)]
    non_X_num = vertices_num-1

    min_heap = MinHeap(vertices_num)
    min_heap.initialize(1, vertices)
    orig = -1
    while non_X_num:
        # optimize with min heap:
        nearest_v, nearest_dist, src = min_heap.extract_min()
        min_heap.update((nearest_v, nearest_dist, src ),vertices, X)
        X.append(nearest_v)
        non_X_num -= 1
        mst[src].append(nearest_v) # TODO: reorder the dsts by x coordinates in order to do pre-order traversal
        print("src: ", src, "nearest_v: ", nearest_v)

    return mst

def nearest_neighbour(vertices, vertices_num):
    X = [1]
    mst = defaultdict(list)
    V = [i for i in range(2, vertices_num+1)]
    non_X_num = vertices_num-1

    min_heap = MinHeap(vertices_num)
    min_heap.initialize(1, vertices)
    src = 1
    while non_X_num:
        if non_X_num % 100 == 0:
            print("the number of vertices left: ", non_X_num)
        nearest_dist = INFINITE
        nearest_v = INFINITE
        for dst in V:
            x1, y1 = vertices[src]
            x2, y2 = vertices[dst]
            d = _distance(x1, y1, x2, y2)
            if d < nearest_dist:
                nearest_dist = d
                nearest_v = dst
            elif d == nearest_dist and dst < nearest_v:
                nearest_dist = d
                nearest_v = dst

        try:
            V.remove(nearest_v) # the nearest_v has been moved to X
        except ValueError:
            print("WARNING: strange nearest_v: ", nearest_v)
        X.append(nearest_v)
        non_X_num -= 1
        mst[src].append(nearest_v) # TODO: reorder the dsts by x coordinates in order to do pre-order traversal
        # print("src: ", src, "nearest_v: ", nearest_v)
        src = nearest_v

    return mst   

def preorder_dfs(mst, vertices):
    # get the preorder traversal of the minimum spanning tree
    ## sort the dsts of each src by their x coordinates
    for src in mst:
        mst[src].sort(key=lambda x: vertices[src][0])

    # dfs
    path = []
    def dfs(t, r):
        path.append(r)
        if r in t.keys():
            assert len(t[r])>0
            for dst in t[r]:
                dfs(t, dst)
    
    def dfs_stack(t, r):
        stack = [r]
        while stack:
            curr = stack.pop()
            path.append(curr)
            if curr in t.keys():
                stack.extend(t[curr])

    dfs_stack(mst, 1)
    print("the path for traversal: ",path)
    return path

def tsp_approx(vertices, vertices_num):
    # create the prim minimum spanning tree ! the assignment require nearest neighbour, but prim is in CRLS
    # mst = mst_prim(vertices, vertices_num)

    # create the path using nearest neighbour
    mst = nearest_neighbour(vertices, vertices_num)
    print("done generating the mst")

    # preorder dfs traversal of the mst:
    path = preorder_dfs(mst, vertices)
    print("done traversing the mst")
    assert len(path) == vertices_num

    # calculate the distance of the for the traveling salesman
    print("to calculate the distance")
    dist = 0
    for i in range(1, vertices_num):
        x1, y1 = vertices[path[i-1]]
        x2, y2 = vertices[path[i]]
        dist += _distance(x1,y1,x2,y2,True)
    x1, y1 = vertices[path[-1]]
    x2, y2 = vertices[path[0]]   
    dist += _distance(x1,y1,x2,y2,True)
    
    return dist

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(1500)
    infile = "nn.txt"
    vertices, vertices_num = readfile(infile)
    dist = tsp_approx(vertices, vertices_num)
    print("resulting distance is: ", dist)