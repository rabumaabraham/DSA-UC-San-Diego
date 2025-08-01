import sys
import math

def get_parent(parent, i):
    if parent[i] == i:
        return i
    parent[i] = get_parent(parent, parent[i])
    return parent[i]

def union_sets(parent, i, j):
    root_i = get_parent(parent, i)
    root_j = get_parent(parent, j)
    if root_i != root_j:
        parent[root_i] = root_j
        return True
    return False

def clustering(x, y, k):
    n = len(x)
    edges = []
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = math.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
            edges.append((dist, i, j))
            
    edges.sort()
    
    parent = list(range(n))
    
    edges_added = 0
    max_d = 0.0
    
    for weight, u, v in edges:
        if union_sets(parent, u, v):
            edges_added += 1
            if edges_added == n - k:
                # We have built an MST with n-k edges, forming k components.
                # The next edge we would add is the minimum distance between any two of these components.
                # This edge is the answer. So, we return the weight of the next edge in the sorted list.
                # Let's return the weight of this current edge. No, that's not right.
                # The distance between any two points in different clusters must be >= d.
                # The last edge we added to get to exactly k clusters has weight `w`. Any other edge
                # we could add has weight >= w. The minimum distance between any two points from
                # different clusters is the weight of the smallest edge that connects two of these k clusters.
                # Since we are iterating through edges in sorted order, this will be the next edge
                # we would add.
                pass
            
            if edges_added == n - k + 1:
                return weight
                
    return max_d

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1:2 * n + 1:2]
    y = data[2:2 * n + 1:2]
    k = data[2 * n + 1]
    
    print("{0:.9f}".format(clustering(x, y, k)))