# python3

# Arguments:
#   * `n` - the number of vertices.
#   * `edges` - list of edges, each edge is a tuple (u, v), 1 <= u, v <= n.
#   * `colors` - list consisting of `n` characters, each belonging to the set {'R', 'G', 'B'}.
# Return value: 
#   * If there exists a proper recoloring, return value is a list containing new colors, similar to the `colors` argument.
#   * Otherwise, return value is None.
def assign_new_colors(n, edges, colors):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)
    
    # Try all possible colorings
    # For each vertex, we need to choose a color different from its current color
    def is_valid_coloring(new_colors):
        # Check that each vertex has a different color from original
        for i in range(n):
            if new_colors[i] == colors[i]:
                return False
        
        # Check that adjacent vertices have different colors
        for u, v in edges:
            if new_colors[u-1] == new_colors[v-1]:
                return False
        
        return True
    
    def backtrack(vertex):
        if vertex == n:
            return is_valid_coloring(new_colors)
        
        # Try all colors except the current one
        for color in ['R', 'G', 'B']:
            if color != colors[vertex]:
                new_colors[vertex] = color
                if backtrack(vertex + 1):
                    return True
        
        return False
    
    new_colors = [''] * n
    if backtrack(0):
        return new_colors
    else:
        return None
    
def main():
    n, m = map(int, input().split())
    colors = list(input().strip())  # Read as string and convert to list
    edges = []
    for i in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))
    new_colors = assign_new_colors(n, edges, colors)
    if new_colors is None:
        print("Impossible")
    else:
        print(''.join(new_colors))

main()
