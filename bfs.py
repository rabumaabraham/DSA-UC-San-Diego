import sys
import collections

def distance(adj, u, v):
    """
    Computes the shortest path length from u to v using BFS.
    """
    n = len(adj) - 1
    dist = [-1] * (n + 1)
    
    # Initialize a queue for BFS
    q = collections.deque()
    
    # Start BFS from vertex u
    dist[u] = 0
    q.append(u)
    
    while q:
        curr_v = q.popleft()
        
        # If we reached the target vertex, return its distance
        if curr_v == v:
            return dist[v]
        
        for neighbor in adj[curr_v]:
            if dist[neighbor] == -1:
                dist[neighbor] = dist[curr_v] + 1
                q.append(neighbor)
                
    # If the queue becomes empty and we haven't reached v, no path exists
    return -1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    u, v = data[2 * m:]
    
    adj = [[] for _ in range(n + 1)]
    for (a, b) in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    print(distance(adj, u, v))