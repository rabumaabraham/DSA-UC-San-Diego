# python3
n, m = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(m) ]

# Implement efficient 2-SAT solver using strongly connected components
def isSatisfiable():
    # Build implication graph
    # For clause (a OR b), add edges: ~a -> b and ~b -> a
    graph = [[] for _ in range(2 * n)]  # 2n vertices: x1, ~x1, x2, ~x2, ...
    
    def get_vertex(var):
        # Convert variable to vertex index
        # Positive variable i -> vertex 2*(i-1)
        # Negative variable -i -> vertex 2*(i-1) + 1
        if var > 0:
            return 2 * (var - 1)
        else:
            return 2 * (-var - 1) + 1
    
    # Build implication graph
    for clause in clauses:
        a, b = clause
        # (a OR b) is equivalent to (~a -> b) AND (~b -> a)
        graph[get_vertex(-a)].append(get_vertex(b))
        graph[get_vertex(-b)].append(get_vertex(a))
    
    # Find strongly connected components using Tarjan's algorithm
    index = [0]
    stack = []
    on_stack = [False] * (2 * n)
    low = [-1] * (2 * n)
    ids = [-1] * (2 * n)
    component = [0] * (2 * n)
    comp_count = [0]
    
    def tarjan(v):
        ids[v] = index[0]
        low[v] = index[0]
        index[0] += 1
        stack.append(v)
        on_stack[v] = True
        
        for u in graph[v]:
            if ids[u] == -1:
                tarjan(u)
                low[v] = min(low[v], low[u])
            elif on_stack[u]:
                low[v] = min(low[v], ids[u])
        
        if low[v] == ids[v]:
            while True:
                u = stack.pop()
                on_stack[u] = False
                component[u] = comp_count[0]
                if u == v:
                    break
            comp_count[0] += 1
    
    # Run Tarjan's algorithm
    for v in range(2 * n):
        if ids[v] == -1:
            tarjan(v)
    
    # Check if formula is satisfiable
    # If x and ~x are in the same SCC, formula is unsatisfiable
    for i in range(n):
        if component[2 * i] == component[2 * i + 1]:
            return None
    
    # Build solution
    assignment = [False] * n
    
    # For each variable, choose the literal with smaller component ID
    for i in range(n):
        pos_comp = component[2 * i]      # component of x_i
        neg_comp = component[2 * i + 1]  # component of ~x_i
        
        # Choose the literal that appears later in the topological order
        # (smaller component ID means later in topological order)
        if pos_comp < neg_comp:
            assignment[i] = False  # Choose ~x_i (negative literal)
        else:
            assignment[i] = True   # Choose x_i (positive literal)
    
    return assignment

result = isSatisfiable()
if result is None:
    print("UNSATISFIABLE")
else:
    print("SATISFIABLE");
    print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
