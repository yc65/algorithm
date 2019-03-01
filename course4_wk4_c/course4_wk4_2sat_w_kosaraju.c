#include "course4_wk4_2sat_w_kosaraju.h"

#define V_NUM 1000000
#define SIZE V_NUM*2
// #define SIZE 9
int TIME = 0;
int RTIME_MAP[SIZE+1] = {0};
int RTIME_MAP_REV[SIZE+1] = {0}; // map from rtime to vertex
bool VISITED[SIZE+1] = {false};
int SCC[SIZE+1] = {0};
int NUM_SCC = 0;

node_t *create_new_node(int * vertex)
{
    node_t * new_node;
    new_node = (node_t *) malloc(sizeof(node_t));
    new_node->vertex = vertex;
    new_node->next = NULL;
    return new_node;
}

void add_adge(graph_t * g, int * src, int * dest)
{
    node_t  *new_node = create_new_node(dest);
    new_node->next = g->arr[*src].head;
    g->arr[*src].head = new_node;
}

void print_graph(graph_t *g)
{
    for (int i=0; i < SIZE+1; i++)
    {
        node_t * node = g->arr[i].head;
        while(node)
        {
            if (node != NULL)
            {
                printf("->%d",  *(node->vertex));
                node = node->next;
            }
        }
        printf("\n");
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

void create_rtime_graph(graph_t *graph_orig, int * vertices, graph_t *graph_rtime)
{
    node_t * node;
    graph_rtime->num_v = graph_orig->num_v;
    for (int i=0; i<graph_orig->num_v; i++)
    {
        graph_rtime->arr[RTIME_MAP[i]] = graph_orig->arr[i];
        node = graph_rtime->arr[RTIME_MAP[i]].head;
        while (node)
        {
            node->vertex = vertices + RTIME_MAP[*(node->vertex)];
            node = node->next;
        }
    }
}

void dfs(graph_t * g, int vertex)
{
    node_t * node = g->arr[vertex].head;
    VISITED[vertex] = true;
    while (node!=NULL)
    {
        if (VISITED[*(node->vertex)] == false)
        {
            dfs(g, *(node->vertex));
        }
        node = node->next;
    }
    TIME++;
    RTIME_MAP[vertex] = TIME;
    RTIME_MAP_REV[TIME] = vertex;
}

void dfs_2(graph_t * g, int vertex, int scc_idx)
{
    node_t * node = g->arr[vertex].head;
    VISITED[vertex] = true;
    while (node!=NULL)
    {
        if (VISITED[*(node->vertex)] == false)
        {
            SCC[RTIME_MAP_REV[*(node->vertex)]] = scc_idx;
            dfs_2(g, *(node->vertex), scc_idx);
        }
        node = node->next;
    }
}

void dfs_loop(graph_t *g)
{
    int n = SIZE;
    int begin = 0; 
    int end = 0;
    int scc;
    int scc_idx=1;
    TIME = 0;
    while (n>0)
    {
        if (VISITED[n] == false)
        {
            dfs(g, n);
            // end = RTIME_MAP[n];
            // scc = end-begin;
            // insert_scc(scc);
            // begin = end;
            scc_idx++;
        }
        n--;
    }
}

void dfs_loop_2(graph_t *g)
{
    int n = SIZE;
    int begin = 0; 
    int end = 0;
    int scc;
    int scc_idx=1;
    TIME = 0;
    while (n>0)
    {
        if (VISITED[n] == false)
        {
            dfs_2(g, n, scc_idx);
            // end = RTIME_MAP[n];
            // scc = end-begin;
            // insert_scc(scc);
            // begin = end;
            scc_idx++;
        }
        n--;
    }
}

bool is_2sat()
{
    int res = 1;
    for (int i = 1; i< V_NUM+1; i++)
    {
        if (SCC[i] == SCC[i+V_NUM] && SCC[i] != 0 && SCC[i+V_NUM] != 0)
        {
            res = 0;
        }
    }
    return res;
}

int main(int argc, char const *argv[])
{
    /* code */
    int * vertices;
    graph_t * g_orig;
    graph_t * g_rev;
    graph_t * g_rtime;
    FILE * fp;
    int start, end;
    bool visited[SIZE+1];

    // allocate memory for all vertices
    vertices = malloc((SIZE+1) * sizeof(int));
    for (int i=0; i< SIZE+1; i++)
    {
        *(vertices+i) = i;
    }

    // allocate memory for g_orig
    g_orig = (graph_t *) malloc(sizeof(graph_t));
    g_orig->num_v = SIZE+1;
    g_orig->arr = (adjList_t *) malloc(g_orig->num_v*sizeof(adjList_t));
    for (int i=0; i<SIZE+1; i++)
    {
        g_orig->arr[i].head = NULL;
    }

    // allocate memory for g_rev
    g_rev = (graph_t *) malloc(sizeof(graph_t));
    g_rev->num_v = SIZE+1;
    g_rev->arr = (adjList_t *) malloc(g_rev->num_v * sizeof(adjList_t));
    for (int i=0; i<SIZE+1; i++)
    {
        g_rev->arr[i].head = NULL;
    }

    // allocate memory for g_rtime
    g_rtime = (graph_t *) malloc(sizeof(graph_t));
    g_rtime->num_v = SIZE+1;
    g_rtime->arr = (adjList_t *) malloc(g_rtime->num_v * sizeof(adjList_t));
    for (int i=0; i<SIZE+1; i++)
    {
        g_rtime->arr[i].head = NULL;
    }

    fp = fopen("2sat6.txt", "r");
	if(!fp)
		printf("Fail to open file\n\n");
	else
		printf("Open file successfully!\n\n");
    
    int size;
    fscanf(fp, "%d", &size);
    // if (size != SIZE)
    // {
    //     fprintf("warning: the vertices number is not correct.\n");
    // }
    int encode_start, encode_end;
    int encode_neg_start, encode_neg_end;
    while (fscanf(fp, "%d %d", &start, &end) != EOF)
    {
        if (start < 0)
        {
            encode_start = V_NUM-start;
            encode_neg_start = 0-start;
        }
        else
        {
            encode_start = start;
            encode_neg_start = V_NUM+start;
        }

        if (end<0)
        {
            encode_end = V_NUM-end;
            encode_neg_end = 0-end;
        }
        else
        {
            encode_end = end;
            encode_neg_end = V_NUM+end;
        }
        
        add_adge(g_orig, vertices+encode_neg_start, vertices+encode_end);
        add_adge(g_orig, vertices+encode_neg_end, vertices+encode_start);
        add_adge(g_rev, vertices+encode_end, vertices+encode_neg_start);
        add_adge(g_rev, vertices+encode_start, vertices+encode_neg_end);
    }

    dfs_loop(g_rev);

    // test:
    // print_graph(g_rev);
    // for (int i = 0; i< SIZE+1; i++)
    // {
    //     printf("%d  %d\n", i,RTIME_MAP[i]);
    // }

    // reset visited and SCC
    for (int i=0; i<SIZE+1; i++)
    {
        VISITED[i] = false;
    }

    for (int i=0; i<5; i++)
    {
        SCC[i] = 0;
    }

    // TODO run dfs on rtime graph and calculate SCCs
    create_rtime_graph(g_orig, vertices, g_rtime);

    // test:
    // print_graph(g_rtime);

    dfs_loop_2(g_rtime);
    int res;
    res = is_2sat();
    printf("res is %d ", res);
    // for (int i=0; i<5; i++)
    // {
    //     printf("%d ", SCC[i]);
    // }
    // for (int i = 0; i< SIZE+1; i++)
    // {
    //     printf("%d  %d\n", i,RTIME_MAP[i]);
    // }
    // printf("test\n");
    free_graph(g_orig);
    free_graph(g_rev);
    // free_graph(g_rtime);
    free(g_rtime);
    return 0;
}
