#include <stdio.h> 
#include <stdlib.h> 

typedef enum{false = 0, true = !false} bool;
typedef struct node{
    int vertex;
    int weight;
    struct node * next;
} node_t;

typedef struct adjList{
    // int num_dst;
    // int num_processed; // if num_dst == num_processed we no longer need to examing the edges starts from this node; no use when using heap
    node_t * head;
} adjList_t;

typedef struct graph{
    int num_v;
    adjList_t * arr;
} graph_t;

typedef struct heap_node{
    int key; // the dijkstra's score
    int vertex;
    int src;
} heap_node_t;

typedef struct heap{
    int heap_num; // record the number of element in the current heap
    int *hash_map; // map from the vertex to location in heap, e.g. vertex 1 -> the 5th element in the heap
    heap_node_t * arr;
} heap_t;

void heap_swap(heap_t *h, int i, int j);
void heap_init(graph_t *g, int start, heap_t * h);
void extract_min(heap_t * h, int * src_v, int *v, int *key) ;
void heap_insert(heap_t * h, int key, int vertex, int src_v);
void heap_delete(heap_t * h, int idx);
void heap_update(graph_t *g, heap_t * h, int vertex);
