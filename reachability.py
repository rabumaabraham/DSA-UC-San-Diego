import sys

def explore(adj, x, y, visited):
    """
    Performs a DFS-like exploration to check for a path from x to y.
    """
    if x == y:
        return True
    
    visited[x] = True
    
    for neighbor in adj[x]:
        if not visited[neighbor]:
            if explore(adj, neighbor, y, visited):
                return True
    
    return False

def reach(adj, x, y):
    """
    Main function to check for reachability.
    """
    visited = [False] * (len(adj))
    return 1 if explore(adj, x, y, visited) else 0

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    x, y = data[2 * m:]
    adj = [[] for _ in range(n + 1)]
    for (a, b) in edges:
        adj[a].append(b)
        adj[b].append(a)
    print(reach(adj, x, y))