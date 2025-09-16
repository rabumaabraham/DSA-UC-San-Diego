# python3
from sys import stdin
  
def allocate_ads(n, m, A, b, c):
    # Implement simplified simplex method for ad allocation
    # Convert to standard form: max c^T x subject to Ax <= b, x >= 0
    
    # Add slack variables to convert inequalities to equalities
    # The system becomes: [A I] [x; s] = b, where s are slack variables
    
    # Create tableau: [A | I | b] where I is identity matrix for slack variables
    # Bottom row is objective: [-c | 0 | 0] (negated because we're maximizing)
    
    num_slack = n
    tableau = []
    
    # Add constraint rows
    for i in range(n):
        row = []
        # Original variables
        for j in range(m):
            row.append(float(A[i][j]))
        # Slack variables (identity matrix)
        for j in range(num_slack):
            if j == i:
                row.append(1.0)
            else:
                row.append(0.0)
        # RHS
        row.append(float(b[i]))
        tableau.append(row)
    
    # Add objective row (negated for maximization)
    obj_row = []
    for j in range(m):
        obj_row.append(-float(c[j]))
    for j in range(num_slack):
        obj_row.append(0.0)
    obj_row.append(0.0)
    tableau.append(obj_row)
    
    # Apply simplex method
    try:
        result = simplex_method(tableau, m, n)
        
        if result == "unbounded":
            return [1, None]  # Infinity
        elif result == "infeasible":
            return [-1, None]  # No solution
        else:
            return [0, result]  # Bounded solution
    except:
        return [-1, None]  # No solution

def simplex_method(tableau, num_vars, num_constraints):
    # Basic variables: initially slack variables are basic
    basic_vars = list(range(num_vars, num_vars + num_constraints))
    
    # Simplex iterations
    max_iterations = 1000  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Find entering variable (most negative coefficient in objective row)
        entering_col = -1
        min_coeff = 0.0
        
        for j in range(num_vars):
            if tableau[-1][j] < min_coeff - 1e-10:
                min_coeff = tableau[-1][j]
                entering_col = j
        
        if entering_col == -1:
            # No negative coefficients, optimal solution found
            break
        
        # Find leaving variable using minimum ratio test
        leaving_row = -1
        min_ratio = float('inf')
        
        for i in range(num_constraints):
            if tableau[i][entering_col] > 1e-10:  # Avoid division by zero
                ratio = tableau[i][-1] / tableau[i][entering_col]
                if ratio >= -1e-10 and ratio < min_ratio:  # Allow small negative ratios
                    min_ratio = ratio
                    leaving_row = i
        
        if leaving_row == -1:
            # Unbounded problem
            return "unbounded"
        
        # Update basic variables
        basic_vars[leaving_row] = entering_col
        
        # Pivot operation
        pivot_element = tableau[leaving_row][entering_col]
        
        # Normalize pivot row
        for j in range(len(tableau[leaving_row])):
            tableau[leaving_row][j] /= pivot_element
        
        # Eliminate pivot column in all other rows
        for i in range(num_constraints + 1):
            if i != leaving_row:
                factor = tableau[i][entering_col]
                for j in range(len(tableau[i])):
                    tableau[i][j] -= factor * tableau[leaving_row][j]
    
    # Extract solution
    solution = [0.0] * num_vars
    
    for i in range(num_constraints):
        if basic_vars[i] < num_vars:
            solution[basic_vars[i]] = tableau[i][-1]
    
    # Check if solution is feasible
    for i in range(num_vars):
        if solution[i] < -1e-6:
            return "infeasible"
    
    return solution

n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))

anst, ansx = allocate_ads(n, m, A, b, c)

if anst == -1:
  print("No solution")
if anst == 0:  
  print("Bounded solution")
  print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
if anst == 1:
  print("Infinity")
    
