import sys

def explore(adj, v, visited):
    """
    Performs DFS from a vertex v to mark all reachable vertices as visited.
    """
    visited[v] = True
    for neighbor in adj[v]:
        if not visited[neighbor]:
            explore(adj, neighbor, visited)

def number_of_components(adj):
    """
    Counts the number of connected components in the graph.
    """
    visited = [False] * (len(adj))
    count = 0
    
    # Iterate through all vertices (1 to n)
    for v in range(1, len(adj)):
        if not visited[v]:
            count += 1
            explore(adj, v, visited)
            
    return count

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
    print(number_of_components(adj))