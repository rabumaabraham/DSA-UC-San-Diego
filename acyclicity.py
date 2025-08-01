import sys

def explore(adj, v, visited, recursion_stack):
    """
    DFS to detect cycles.
    visited[v] = 1 means currently in recursion stack (gray).
    visited[v] = 2 means finished exploring (black).
    """
    visited[v] = 1 # Mark as visiting
    recursion_stack[v] = True

    for neighbor in adj[v]:
        if not visited[neighbor]:
            if explore(adj, neighbor, visited, recursion_stack):
                return True
        elif recursion_stack[neighbor]: # If neighbor is in recursion stack, we found a back edge
            return True

    recursion_stack[v] = False
    visited[v] = 2 # Mark as visited
    return False

def has_cycle(adj):
    """
    Checks if a directed graph contains a cycle.
    """
    n = len(adj) - 1
    visited = [0] * (n + 1)
    recursion_stack = [False] * (n + 1)
    
    for i in range(1, n + 1):
        if not visited[i]:
            if explore(adj, i, visited, recursion_stack):
                return 1
    return 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    adj = [[] for _ in range(n + 1)]
    for (a, b) in edges:
        adj[a].append(b)
    print(has_cycle(adj))