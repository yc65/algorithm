#include "dijkstra.h"

// #define TEST
#define FINAL

#ifdef FINAL
#define SIZE 200
#endif

#ifdef TEST
#define SIZE 200
#endif

#define INFINIT 10000

int SHORTEST_PATH[SIZE+1] = {-1};
int X[SIZE+1] = {0};

node_t * create_node(int vertex, int weight)
{
    node_t *new_node;
    new_node = (node_t *)malloc(sizeof(node_t));
    new_node->vertex = vertex;
    new_node->weight = weight;
    new_node->next = NULL;
    return new_node;
}

void add_edge(graph_t * g, int src, int dest, int weight)
{
    node_t *new_node = create_node(dest, weight);
    new_node->next = g->arr[src].head;
    g->arr[src].head = new_node;
}

void print_graph(graph_t *g)
{
    for (int i=0; i<g->num_v; i++)
    {
        node_t * node = g->arr[i].head;
        printf("vertex: %d\n", i);
        while(node != NULL)
        {
            printf("->%d,%d", node->vertex, node->weight);
            node = node->next;
        }
        printf("\n");
    }
}

void heap_swap(heap_t *h, int i, int j)
{
    heap_node_t temp;
    h->hash_map[h->arr[i].vertex] = j;
    h->hash_map[h->arr[j].vertex] = i;
    temp = h->arr[i];
    h->arr[i] = h->arr[j];
    h->arr[j] = temp;

}

// initialize the heap to contain w in (1, w)
void heap_init(graph_t *g, int start, heap_t * h)
{
    printf("enter heap_init\n");
    int visited[SIZE+1] = {false};
    // get the dst of start (1) and add them to heap
    SHORTEST_PATH[start] = 0;
    // EXTRACTED[start] = true;
    // COUNT ++;
    node_t *dst_node;
    dst_node = g->arr[start].head;
    // !!!!!!note heap should be initialized for all V-X!!! use a large number as the initialized key!
    while (dst_node != NULL)
    {
        heap_insert(h, dst_node->weight+SHORTEST_PATH[start], dst_node->vertex, start);
        visited[dst_node->vertex] = true;
        dst_node = dst_node->next;
    }
    for (int i = 2; i<=SIZE; i++)
    {
        if (visited[i] == false)
        {
            heap_insert(h,INFINIT,i, -1);
        }
    }

}

// return the smallest dijkstra score as well as the src vertex and dst vertex
void extract_min(heap_t * h, int * src_v, int *v, int *key) 
{
    int curr_id = 1;
    int lchild_id, rchild_id;
    *src_v = h->arr[1].src;
    *v = h->arr[1].vertex;
    *key = h->arr[1].key;
    heap_swap(h, 1, h->heap_num);
    //delete the last node TODO wrap this into heap_delete
    h->hash_map[h->arr[h->heap_num].vertex] = 0;
    h->arr[h->heap_num].key = 0;
    h->arr[h->heap_num].vertex = 0;
    h->arr[h->heap_num].src = 0;
    h->heap_num--;
    //bubble down
    lchild_id = curr_id * 2;
    rchild_id = curr_id * 2 + 1;
    // !!!!!! note we need to chose the smaller child before bubbling down!!!
    while ( curr_id < h->heap_num)
        if ((lchild_id <=h->heap_num && h->arr[lchild_id].key < h->arr[curr_id].key)||
            (rchild_id<=h->heap_num && h->arr[rchild_id].key < h->arr[curr_id].key))
        {
            if (h->arr[lchild_id].key < h->arr[rchild_id].key )
            {
                heap_swap(h, curr_id, lchild_id);
                curr_id = lchild_id;
                lchild_id = curr_id*2;
                rchild_id = curr_id*2+1;
            }
            else
            {
                heap_swap(h, curr_id, rchild_id);
                curr_id = rchild_id;
                lchild_id = curr_id * 2;
                rchild_id = curr_id * 2 + 1;
            }
        }
        else{break;}
}

void heap_insert(heap_t * h, int key, int vertex, int src_v) // src_v never used, could be deleted
{
    int curr_id, parent_id;
    curr_id = h->heap_num+1;
    // insert in the end
    h->arr[curr_id].key = key;
    h->arr[curr_id].vertex = vertex;
    h->arr[curr_id].src = src_v;

    h->hash_map[vertex] = curr_id;
    
    parent_id = (int)(curr_id/2);
    while (parent_id != 0 && h->arr[curr_id].key < h->arr[parent_id].key)
    {
        heap_swap(h, curr_id, parent_id);
        curr_id = parent_id;
        parent_id = (int)(parent_id/2);
        if (curr_id == 1)
        {
            break;
        }
    }

    h->heap_num++;
}

void heap_delete(heap_t * h, int idx)
{
    int curr_id = idx;
    int parent_id = (int) curr_id/2;
    int lchild_id = curr_id *2;
    int rchild_id = curr_id * 2+1;
    // swap with the last in the heap
    heap_swap(h, idx, h->heap_num);
    // delete the last one in the heap
    h->hash_map[h->arr[h->heap_num].vertex] = 0;
    h->arr[h->heap_num].key = 0;
    h->arr[h->heap_num].vertex = 0;
    h->arr[h->heap_num].src = 0;
    h->heap_num--;
    //bubble up/down
    if (idx <= h->heap_num && h->arr[idx].key < h->arr[parent_id].key && idx != 1)
    {
        // bubble up
        while (h->arr[idx].key < h->arr[parent_id].key && idx != 1)
        {
            heap_swap(h, idx, parent_id);
            idx = parent_id;
            parent_id = (int) idx/2;
        }
    }
    else if ((lchild_id < h->heap_num && h->arr[idx].key > h->arr[lchild_id].key) 
            || (rchild_id<=h->heap_num && h->arr[rchild_id].key < h->arr[curr_id].key))
    {
        // bubble down
        while ( curr_id < h->heap_num)
            if (lchild_id <=h->heap_num && h->arr[lchild_id].key < h->arr[curr_id].key )
            {
                heap_swap(h, curr_id, lchild_id);
                curr_id = lchild_id;
                lchild_id = curr_id*2;
                rchild_id = curr_id*2+1;
            }
            else if (rchild_id<=h->heap_num && h->arr[rchild_id].key < h->arr[curr_id].key)
            {
                heap_swap(h, curr_id, rchild_id);
                curr_id = rchild_id;
                lchild_id = curr_id * 2;
                rchild_id = curr_id * 2 + 1;
            }
            else
            {
                break;
            }
    }

}   

// int RECUR_COUNT = 0;
// int VISITED[SIZE] = {false};
void heap_update(graph_t *g, heap_t * h, int vertex) // vertex is the one just moved to X
{
    printf("enter heap_update %d\n", vertex);
    node_t * dst_node;
    dst_node = g->arr[vertex].head;
    // VISITED[vertex] = true;
    while (dst_node)
    {
        int heap_id = h->hash_map[dst_node->vertex];
        int key;
        
        if (heap_id != 0) // the dst is in the heap
        {
            key = h->arr[heap_id].key;
            
            if (SHORTEST_PATH[vertex] + dst_node->weight < key)
            {
                key = SHORTEST_PATH[vertex] + dst_node->weight;
                heap_delete(h, heap_id);
                heap_insert(h, key, dst_node->vertex, vertex);
            }
        }
        dst_node = dst_node->next;
    }

}

void free_graph(graph_t *g)
{
    if (g!=NULL)
    {
        if (g->arr!=NULL)
        {
            for (int i = 0; i < g->num_v; i++)
            {
                adjList_t * adjList = &(g->arr[i]);
                if (adjList!=NULL)
                {
                    node_t * node = adjList->head;
                    while (node!=NULL)
                    {
                        node_t * node_temp = node;
                        node = node->next;
                        free(node_temp);
                        node_temp = NULL;
                    }
                    adjList->head = NULL;
                }
            }
            free(g->arr);
            g->arr = NULL;
        }
        free(g);
        g = NULL;
    }
}

int main(int argc, char const *argv[])
{
    FILE * fp;
    graph_t *graph;
    graph = (graph_t *) malloc(sizeof(graph_t));
    graph->num_v = SIZE+1;
    graph->arr = (adjList_t*)malloc(sizeof(adjList_t)*(SIZE+1));
    for (int i=0; i<SIZE+1;i++)
    {
        graph->arr[i].head = NULL;
    }
#ifdef FINAL
    fp = fopen("dijkstraData.txt", "r");
#endif

#ifdef TEST
    fp = fopen("input_random_3_4.txt", "r");
    // fp = fopen("test2.txt", "r");
#endif

    
    if (!fp)
    {
        printf("ERROR: cannot open the data file");
    }
    else{
        printf("data file opened successfully\n");
    }
    printf("test after readingfile\n");
    // create graph
    int temp;
    int weight = -1;
    int src;
    int dst;
    char c[4];
    // char c[2];
    bool reset = true;

    while (1) 
    {
        int ret;
        if (reset == true)
        {
            printf("seek src\n");
            ret = fscanf(fp, "%d", &temp);
            if (ret == EOF) break;
            src = temp;
            reset = false;
            weight = -1;
        }
        else
        {
            ret = fscanf(fp, "%d,%d", &temp, &weight);
            if (ret == EOF) break;
            dst = temp;
        }
        if (weight != -1)
        {
#ifdef FINAL
            fgets(c, 4, fp);
            if (c[2] == '\n') {reset = true;}
            fseek(fp, -3L, SEEK_CUR);
#endif
#ifdef TEST
            fgets(c, 2, fp);
            if (c[0] == '\n') {reset = true;}
            fseek(fp, -1L, SEEK_CUR);
#endif
            add_edge(graph, src, dst, weight);
            printf("%d  %d  %d\n", src, dst, weight);
        }
    }

    // test:print graph
    print_graph(graph);

    // initialize heap
    heap_t *h;
    h = (heap_t *) malloc(sizeof(heap_t));
    h->heap_num = 0; 
    h->hash_map = (int*) calloc (SIZE+1, sizeof(int));
    h->arr = (heap_node_t *) malloc(sizeof(heap_node_t) * SIZE);

    heap_init(graph, 1, h);

    int X_num = 0;
    *(X+X_num) = 1;
    X_num++;

    // dijkstra
    int vertex;
    int key;
    int src_v;
    // printf("testabc");
    while (h->heap_num>0)
    {
        // printf("heap_num: %d", h->heap_num);
        extract_min(h, &src_v, &vertex, &key);
        printf("src: %d  vertex: %d   key: %d\n", src_v,vertex, key);
        SHORTEST_PATH[vertex] = key;
        *(X+X_num) = vertex;
        X_num ++;
        if (X_num == SIZE)
        {break;}
        heap_update(graph, h, vertex);
    }
#ifdef FINAL
    //7,37,59,82,99,115,133,165,188,197
    for (int i=0; i< SIZE+1; i++)
    {
        if (i==7 || i==37 || i==59 || i==82 || i==99 || i==115 || i==133 || i==165 || i==188 || i==197)
        printf("%d,", SHORTEST_PATH[i]);
    }
    printf("\n");
#endif

#ifdef TEST
    for (int i=0; i< SIZE+1; i++)
    {
        printf("%d  %d\n", i,SHORTEST_PATH[i]);
    }
    for (int i=0; i< SIZE+1; i++)
    {
        if (i==7 || i==37 || i==59 || i==82 || i==99 || i==115 || i==133 || i==165 || i==188 || i==197)
        printf("%d,", SHORTEST_PATH[i]);
    }
#endif
    // free
    free_graph(graph);

    // h = (heap_t *) malloc(sizeof(heap_t));
    // h->heap_num = 0; 
    // h->hash_map = (int*) calloc (SIZE+1, sizeof(int));
    // h->arr = (heap_node_t *) malloc(sizeof(heap_node_t) * SIZE);
    free(h->arr);
    free(h->hash_map);
    free(h);

    printf("test\n");
    return 0;
}
