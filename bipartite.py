import sys
import collections

def is_bipartite(adj):
    """
    Checks if a graph is bipartite using BFS-based coloring.
    """
    n = len(adj) - 1
    color = [0] * (n + 1)
    
    # Iterate through all vertices in case the graph is disconnected
    for i in range(1, n + 1):
        if color[i] == 0:
            q = collections.deque()
            q.append(i)
            color[i] = 1
            
            while q:
                curr_v = q.popleft()
                for neighbor in adj[curr_v]:
                    if color[neighbor] == 0:
                        # Color the neighbor with the opposite color
                        color[neighbor] = 3 - color[curr_v]
                        q.append(neighbor)
                    elif color[neighbor] == color[curr_v]:
                        # Found an edge with endpoints of the same color
                        return 0
                        
    return 1

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n + 1)]
    for (a, b) in edges:
        adj[a].append(b)
        adj[b].append(a)
    
    print(is_bipartite(adj))