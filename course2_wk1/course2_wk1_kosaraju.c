#include "kosaraju.h"

#define SIZE 875714
// #define SIZE 9
int TIME = 0;
int RTIME_MAP[SIZE+1] = {0};
bool VISITED[SIZE+1] = {false};
int SCC[5] = {0};
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
}

void sort_scc()
{
    int n = NUM_SCC-1;
    int temp;
    while (n>0)
    {
        if (SCC[n-1]<SCC[n])
        {
            temp = SCC[n];
            SCC[n] = SCC[n-1];
            SCC[n-1] = temp;
            n--;
        }
        else
        {
            break;
        }
    }
}

void insert_scc(int s)
{
    if (NUM_SCC < 5)
    {
        SCC[NUM_SCC] = s;
        NUM_SCC++;
        sort_scc();
    }
    else
    {
        if (SCC[4] < s)
        {
            SCC[4] = s;
            sort_scc();
        }
    }
}

void dfs_loop(graph_t *g)
{
    int n = SIZE;
    int begin = 0; 
    int end = 0;
    int scc;
    TIME = 0;
    while (n>0)
    {
        if (VISITED[n] == false)
        {
            dfs(g, n);
            end = RTIME_MAP[n];
            scc = end-begin;
            insert_scc(scc);
            begin = end;
        }
        n--;
    }
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

    fp = fopen("SCC.txt", "r");
	if(!fp)
		printf("Fail to open file\n\n");
	else
		printf("Open file successfully!\n\n");
    
    while (fscanf(fp, "%d %d", &start, &end) != EOF)
    {
        add_adge(g_orig, vertices+start, vertices+end);
        add_adge(g_rev, vertices+end, vertices+start);
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

    dfs_loop(g_rtime);

    for (int i=0; i<5; i++)
    {
        printf("%d ", SCC[i]);
    }
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
