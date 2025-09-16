# python3
from itertools import permutations
INF = 10 ** 9

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    return graph

def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))

def optimal_path(graph):
    # Solve TSP using dynamic programming with bitmasking
    n = len(graph)
    
    # dp[mask][i] = minimum cost to visit all cities in mask ending at city i
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    
    # Initialize: starting from city 0
    dp[1][0] = 0
    
    # Fill DP table
    for mask in range(1, 1 << n):
        for i in range(n):
            if not (mask & (1 << i)) or dp[mask][i] == INF:
                continue
            
            for j in range(n):
                if mask & (1 << j) or graph[i][j] == INF:
                    continue
                
                new_mask = mask | (1 << j)
                if dp[mask][i] + graph[i][j] < dp[new_mask][j]:
                    dp[new_mask][j] = dp[mask][i] + graph[i][j]
                    parent[new_mask][j] = i
    
    # Find the best solution that visits all cities and returns to start
    full_mask = (1 << n) - 1
    best_cost = INF
    best_end = -1
    
    for i in range(n):
        if dp[full_mask][i] != INF and graph[i][0] != INF:
            total_cost = dp[full_mask][i] + graph[i][0]
            if total_cost < best_cost:
                best_cost = total_cost
                best_end = i
    
    if best_cost == INF:
        return (-1, [])
    
    # Reconstruct the path
    path = []
    mask = full_mask
    current = best_end
    
    while current != -1:
        path.append(current)
        new_mask = mask ^ (1 << current)
        current = parent[mask][current]
        mask = new_mask
    
    path.reverse()
    return (best_cost, [x + 1 for x in path])


if __name__ == '__main__':
    print_answer(*optimal_path(read_data()))
