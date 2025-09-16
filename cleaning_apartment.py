# python3
n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

def printEquisatisfiableSatFormula():
    # Convert Hamiltonian Path problem to SAT
    # Variables: x[i][j] = True if vertex i is in position j of the path
    # We need to ensure:
    # 1. Each vertex appears exactly once in the path
    # 2. Each position has exactly one vertex
    # 3. Consecutive vertices in the path must be connected by an edge
    
    # Create adjacency list for quick edge lookup
    adj = [[] for _ in range(n + 1)]  # 1-indexed vertices
    for edge in edges:
        u, v = edge
        adj[u].append(v)
        adj[v].append(u)
    
    # Variables: x[i][j] where i is vertex (1 to n) and j is position (1 to n)
    # Variable number: (i-1) * n + j
    def var_num(vertex, position):
        return (vertex - 1) * n + position
    
    clauses = []
    
    # 1. Each vertex appears at least once
    for i in range(1, n + 1):
        clause = []
        for j in range(1, n + 1):
            clause.append(var_num(i, j))
        clause.append(0)
        clauses.append(clause)
    
    # 2. Each vertex appears at most once
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(j + 1, n + 1):
                clauses.append([-var_num(i, j), -var_num(i, k), 0])
    
    # 3. Each position has at least one vertex
    for j in range(1, n + 1):
        clause = []
        for i in range(1, n + 1):
            clause.append(var_num(i, j))
        clause.append(0)
        clauses.append(clause)
    
    # 4. Each position has at most one vertex
    for j in range(1, n + 1):
        for i in range(1, n + 1):
            for k in range(i + 1, n + 1):
                clauses.append([-var_num(i, j), -var_num(k, j), 0])
    
    # 5. Consecutive positions must be connected by an edge
    for j in range(1, n):
        for i in range(1, n + 1):
            # If vertex i is in position j, then position j+1 must have a neighbor of i
            clause = [-var_num(i, j)]
            for neighbor in adj[i]:
                clause.append(var_num(neighbor, j + 1))
            clause.append(0)
            clauses.append(clause)
    
    # Print SAT formula in DIMACS format
    num_vars = n * n
    print("{} {}".format(len(clauses), num_vars))
    for clause in clauses:
        print(" ".join(map(str, clause)))

printEquisatisfiableSatFormula()
