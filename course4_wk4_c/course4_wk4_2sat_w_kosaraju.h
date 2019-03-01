#ifndef kosaraju_h
#define kosaraju_h

#include <stdio.h> 
#include <stdlib.h> 
typedef enum {false = 0, true = !false} bool;
typedef struct node 
{
    int * vertex;
    struct node *next; 
} node_t;

typedef struct adjList
{
    struct node * head;
} adjList_t;

typedef struct graph
{
    int num_v;
    struct adjList * arr;
} graph_t;

#endif