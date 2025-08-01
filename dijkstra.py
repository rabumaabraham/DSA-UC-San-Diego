import sys
import heapq

def dijkstra(adj, cost, u, v):
    """
    Computes the shortest path length from u to v using Dijkstra's algorithm.
    """
    n = len(adj) - 1
    dist = [float('inf')] * (n + 1)
    
    # Priority queue stores (distance, vertex) tuples
    pq = [(0, u)]
    dist[u] = 0
    
    while pq:
        d, curr_v = heapq.heappop(pq)
        
        # If we have already found a shorter path, skip
        if d > dist[curr_v]:
            continue
            
        if curr_v == v:
            return dist[v]
        
        for i in range(len(adj[curr_v])):
            neighbor = adj[curr_v][i]
            weight = cost[curr_v][i]
            
            if dist[curr_v] + weight < dist[neighbor]:
                dist[neighbor] = dist[curr_v] + weight
                heapq.heappush(pq, (dist[neighbor], neighbor))
                
    return dist[v] if dist[v] != float('inf') else -1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(3 * m):3], data[1:(3 * m):3], data[2:(3 * m):3]))
    u, v = data[3 * m:]
    
    adj = [[] for _ in range(n + 1)]
    cost = [[] for _ in range(n + 1)]
    for (a, b, w) in edges:
        adj[a].append(b)
        cost[a].append(w)
    
    print(dijkstra(adj, cost, u, v))