import sys

# We need to increase recursion limit for deep graphs
sys.setrecursionlimit(200000)

def explore1(adj, v, visited, order):
    """
    First DFS pass on the original graph to compute finishing times.
    """
    visited[v] = True
    for neighbor in adj[v]:
        if not visited[neighbor]:
            explore1(adj, neighbor, visited, order)
    order.append(v)

def explore2(adj, v, visited):
    """
    Second DFS pass on the transpose graph to find SCCs.
    """
    visited[v] = True
    for neighbor in adj[v]:
        if not visited[neighbor]:
            explore2(adj, neighbor, visited)

def number_of_strongly_connected_components(adj):
    """
    Computes the number of strongly connected components using Kosaraju's algorithm.
    """
    n = len(adj) - 1
    visited = [False] * (n + 1)
    order = []
    
    # First DFS pass to compute finishing times
    for v in range(1, n + 1):
        if not visited[v]:
            explore1(adj, v, visited, order)
    
    # Build transpose graph
    adj_rev = [[] for _ in range(n + 1)]
    for v in range(1, n + 1):
        for neighbor in adj[v]:
            adj_rev[neighbor].append(v)
            
    # Second DFS pass on transpose graph
    visited = [False] * (n + 1)
    scc_count = 0
    
    # Iterate through vertices in decreasing order of finishing times
    # which is the reverse of the 'order' list.
    while order:
        v = order.pop()
        if not visited[v]:
            explore2(adj_rev, v, visited)
            scc_count += 1
            
    return scc_count

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n + 1)]
    for (a, b) in edges:
        adj[a].append(b)
    
    print(number_of_strongly_connected_components(adj))