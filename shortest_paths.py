import sys

def dfs_visit_inf(adj, v, has_inf_dist):
    """
    Performs DFS to mark all nodes reachable from a negative cycle as having dist = -inf.
    """
    has_inf_dist[v] = True
    for neighbor in adj[v]:
        if not has_inf_dist[neighbor]:
            dfs_visit_inf(adj, neighbor, has_inf_dist)

def shortest_paths(adj, cost, s):
    """
    Computes shortest paths from s, handling negative cycles.
    """
    n = len(adj) - 1
    dist = [float('inf')] * (n + 1)
    dist[s] = 0
    
    # Bellman-Ford
    for i in range(n):
        for u in range(1, n + 1):
            for j in range(len(adj[u])):
                v = adj[u][j]
                weight = cost[u][j]
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight

    # Find vertices whose distance can still be relaxed
    has_inf_dist = [False] * (n + 1)
    
    for u in range(1, n + 1):
        for j in range(len(adj[u])):
            v = adj[u][j]
            weight = cost[u][j]
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                if not has_inf_dist[v]:
                    dfs_visit_inf(adj, v, has_inf_dist)
                    
    # Output results
    for i in range(1, n + 1):
        if dist[i] == float('inf'):
            print('*')
        elif has_inf_dist[i]:
            print('-')
        else:
            print(dist[i])

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(3 * m):3], data[1:(3 * m):3], data[2:(3 * m):3]))
    s = data[3 * m]
    
    adj = [[] for _ in range(n + 1)]
    cost = [[] for _ in range(n + 1)]
    for (a, b, w) in edges:
        adj[a].append(b)
        cost[a].append(w)
    
    shortest_paths(adj, cost, s)