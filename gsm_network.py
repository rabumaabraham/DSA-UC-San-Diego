# python3
n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

def printEquisatisfiableSatFormula():
    # Convert GSM Network problem to SAT
    # This is likely a graph coloring problem where we need to color
    # the vertices with 3 colors such that adjacent vertices have different colors
    # GSM networks typically use 3 frequencies to avoid interference
    
    # Variables: x[i][c] = True if vertex i is colored with color c
    # Colors: 1, 2, 3 (representing different frequencies)
    
    num_colors = 3
    
    # Variable number: (i-1) * num_colors + c
    def var_num(vertex, color):
        return (vertex - 1) * num_colors + color
    
    clauses = []
    
    # 1. Each vertex must be colored with exactly one color
    for i in range(1, n + 1):
        # At least one color
        clause = []
        for c in range(1, num_colors + 1):
            clause.append(var_num(i, c))
        clause.append(0)
        clauses.append(clause)
        
        # At most one color
        for c1 in range(1, num_colors + 1):
            for c2 in range(c1 + 1, num_colors + 1):
                clauses.append([-var_num(i, c1), -var_num(i, c2), 0])
    
    # 2. Adjacent vertices must have different colors
    for edge in edges:
        u, v = edge
        for c in range(1, num_colors + 1):
            clauses.append([-var_num(u, c), -var_num(v, c), 0])
    
    # Print SAT formula in DIMACS format
    num_vars = n * num_colors
    print("{} {}".format(len(clauses), num_vars))
    for clause in clauses:
        print(" ".join(map(str, clause)))

printEquisatisfiableSatFormula()
