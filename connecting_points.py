import sys
import math

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

def minimum_distance(x, y):
    """
    Computes the minimum total length of roads to connect all cities.
    """
    n = len(x)
    edges = []
    
    # Generate all possible edges and their weights (distances)
    for i in range(n):
        for j in range(i + 1, n):
            dist = math.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
            edges.append((dist, i, j))
            
    # Sort edges by weight
    edges.sort()
    
    dsu = DSU(n)
    total_weight = 0
    edges_count = 0
    
    for weight, u, v in edges:
        if dsu.union(u, v):
            total_weight += weight
            edges_count += 1
            if edges_count == n - 1:
                break
                
    return total_weight

if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1:2 * n + 1:2]
    y = data[2:2 * n + 1:2]
    print("{0:.9f}".format(minimum_distance(x, y)))




    