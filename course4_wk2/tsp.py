# -*- coding: utf-8 -*- 
import codecs
import math

INFINITE = 10000000

def read_file(infile):
    cities_num = 0
    cities_coord = [(0,0)] # [(x1, y1), (x2, y2) ...]
    with codecs.open(infile, 'r', 'utf-8') as fi:
        fdata = fi.readline()
        cities_num = int(fdata.strip())
        fdata = fi.readline()
        while fdata:
            temp_x, temp_y = fdata.strip().split(' ')
            cities_coord.append((float(temp_x), float(temp_y)))
            fdata = fi.readline()
    return cities_coord, cities_num

def dfs(arr, start):
    arr_len = len(arr)
    def find_paths(root, arr, path, result):
        # print("find_paths: ", root)
        lchild = root * 2
        rchild = root * 2 + 1
        if lchild>=arr_len:
            # print("reach the leaf")
            result.append(path+str(arr[root]))
        if lchild < arr_len:
            # !!! Note: the following commentted two lines won't work! the path shouldn't be changed, only when it goes into the next recursive call should it be changed
            # path.append(arr[root])
            # find_paths(lchild, arr, path, result)
            # !!! Note: the following commented line won't work either, when getting into the next recursive call, path+str(arr[root])+"-" becomes None
            # find_paths(lchild, arr, path.append(arr[root]), result)
            # !!! Note: str works fine. See also leedcode 257
            # print("recurse on the lchild")
            find_paths(lchild, arr, path+str(arr[root]), result)
        if rchild < arr_len:
            # print("recurse on the rchild")
            find_paths(rchild, arr, path+str(arr[root]),result)
    result = []
    find_paths(start, arr, "", result)
    return result

def calc_sum_samebase_increasing_power(base, num):
    # calculate x**0+x**1+x**2+x**3..+x**num
    res = 0
    for i in range(0, num+1):
        res += base**i
    return res

def distance(j, k, cities_coord):
    # calculate the distance between two cities
    j_x = cities_coord[j][0]
    j_y = cities_coord[j][1]
    k_x = cities_coord[k][0]
    k_y = cities_coord[k][1]
    res = math.sqrt((k_y-j_y)**2+(k_x-j_x)**2)
    return res

def tsp(cities_coord, cities_num):
    # step1: start with the vertex 1
    # step2: use bitmask to represent all possible sets of vertices
    ## create all possible vertices combinations; 
    print("create all possible vertices combinations; ")
    t = [0, 1]*int((1+calc_sum_samebase_increasing_power(2, cities_num-1))/2)# array representation of coding of tree of all possible vertices, dfs to get all possible vertices
    cities_set = dfs(t, 1)
    ## encode the cities with binary int
    city_codes = [(int(i, 2)) for i in cities_set]
    print([bin(i) for i in city_codes])

    def city_set_exclude_j(city_code, city_to_remove):
        # get the city_set - city_j
        new_city_code = 0
        if (city_code>>(cities_num-city_to_remove))&1 == 1:
            new_city_code = city_code - (1<<(cities_num-city_to_remove))
        return new_city_code
    # temp = city_set_exclude_j(city_codes[-1], 3)
    # print(bin(temp))
    city_codes_to_idx = {}
    for i in range(len(city_codes)):
        city_codes_to_idx[city_codes[i]] = i

    # step3: dp
    cache = [[0] * (cities_num+1) for i in range(len(city_codes))]
    ## initialize
    print("initialize the city code: ")
    for i in range(len(city_codes)):
        # print("initialize the city code: ", i)
        cache[i][0] = 0
        cache[i][1] = INFINITE
    cache[0][1] = 0

    ## dp loop
    print("process for dp")
    for s in range(len(city_codes)):
        for j in range(2, cities_num+1):
            min_dist = INFINITE
            for k in range(1, cities_num+1):
                # print("processing for s, j, k: ", s, j, k)
                if k != j:
                    city_code_exclude_j = city_set_exclude_j(city_codes[s],j)
                    if city_code_exclude_j != 0:
                        candidate = cache[city_codes_to_idx[city_code_exclude_j]][k] + distance(j, k,cities_coord)
                        if candidate < min_dist:
                            min_dist = candidate
            cache[s][j] = min_dist
    min_dist = INFINITE
    for j in range(2, cities_num+1):
        candidiate = cache[len(city_codes)-1][j] + distance(j, 1, cities_coord)
        if candidiate < min_dist:
            min_dist = candidiate
    
    return min_dist

if __name__ == "__main__":
    infile = "tsp.txt"
    cities_coord, cities_num = read_file(infile)
    # arr = [0,1,0,1,0,1,0,1]
    # print(dfs(arr, 1))
    # print(calc_sum_samebase_increasing_power(2, 3))x
    res = tsp(cities_coord, cities_num)
    print(res)
    