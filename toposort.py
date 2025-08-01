import sys

def dfs(adj, v, visited, order):
    """
    DFS-based topological sort.
    """
    visited[v] = True
    for neighbor in adj[v]:
        if not visited[neighbor]:
            dfs(adj, neighbor, visited, order)
    
    # Add vertex to the list after visiting all its neighbors
    order.append(v)

def toposort(adj):
    """
    Computes a topological ordering of the graph.
    """
    n = len(adj) - 1
    visited = [False] * (n + 1)
    order = []
    
    for v in range(1, n + 1):
        if not visited[v]:
            dfs(adj, v, visited, order)
            
    # The order is collected in reverse, so we reverse the list
    order.reverse()
    return order

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n + 1)]
    for (a, b) in edges:
        adj[a].append(b)
    
    order = toposort(adj)
    print(*order)