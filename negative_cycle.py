import sys

def negative_cycle(adj, cost):
    """
    Checks for a negative cycle using the Bellman-Ford algorithm.
    """
    n = len(adj) - 1
    dist = [float('inf')] * (n + 1)
    dist[1] = 0 # Can start from any vertex, we choose 1
    
    # Relax all edges n-1 times
    for _ in range(n - 1):
        for u in range(1, n + 1):
            for i in range(len(adj[u])):
                v = adj[u][i]
                weight = cost[u][i]
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    
    # nth relaxation pass to check for negative cycles
    for u in range(1, n + 1):
        for i in range(len(adj[u])):
            v = adj[u][i]
            weight = cost[u][i]
            if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                return 1 # Negative cycle detected
                
    return 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(3 * m):3], data[1:(3 * m):3], data[2:(3 * m):3]))
    adj = [[] for _ in range(n + 1)]
    cost = [[] for _ in range(n + 1)]
    for (a, b, w) in edges:
        adj[a].append(b)
        cost[a].append(w)
    
    print(negative_cycle(adj, cost))