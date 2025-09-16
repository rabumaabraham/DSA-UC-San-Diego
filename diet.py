# python3
from sys import stdin
  
def solve_diet_problem(n, m, A, b, c):
    # First solve without artificial constraint
    best_value = float('-inf')
    best_solution = None
    solution_exists = False
    
    # Try all combinations of m inequalities from n+m total inequalities
    total_inequalities = n + m  # n regular + m non-negativity constraints
    
    # Generate all combinations of size m
    from itertools import combinations
    
    for combo in combinations(range(total_inequalities), m):
        # Create system of equations
        equations = []
        rhs = []
        
        for idx in combo:
            if idx < n:
                # Regular inequality: A[idx] * x = b[idx]
                equations.append(A[idx][:])
                rhs.append(b[idx])
            else:
                # Non-negativity constraint: x[idx-n] = 0
                var_idx = idx - n
                eq = [0.0] * m
                eq[var_idx] = 1.0
                equations.append(eq)
                rhs.append(0.0)
        
        # Solve the system using Gaussian elimination
        try:
            solution = solve_system(equations, rhs, m)
            if solution is not None:
                # Check if solution satisfies all inequalities
                if satisfies_all_constraints(solution, A, b, m):
                    solution_exists = True
                    # Calculate objective value
                    obj_value = sum(solution[i] * c[i] for i in range(m))
                    
                    if obj_value > best_value:
                        best_value = obj_value
                        best_solution = solution[:]
        except:
            continue
    
    if not solution_exists:
        return [-1, None]  # No solution
    
    # Check if we can improve the solution infinitely
    # Add artificial constraint and check if it's tight
    A_art = [row[:] for row in A]
    b_art = b[:]
    A_art.append([1] * m)
    b_art.append(10**9)
    n_art = n + 1
    
    # Try with artificial constraint
    total_inequalities_art = n_art + m
    
    for combo in combinations(range(total_inequalities_art), m):
        equations = []
        rhs = []
        
        for idx in combo:
            if idx < n_art:
                equations.append(A_art[idx][:])
                rhs.append(b_art[idx])
            else:
                var_idx = idx - n_art
                eq = [0.0] * m
                eq[var_idx] = 1.0
                equations.append(eq)
                rhs.append(0.0)
        
        try:
            solution = solve_system(equations, rhs, m)
            if solution is not None and satisfies_all_constraints(solution, A, b, m):
                # If this uses the artificial constraint and improves objective
                if (n_art-1) in combo:
                    obj_value = sum(solution[i] * c[i] for i in range(m))
                    if obj_value > best_value + 1e-6:
                        # Check if any positive coefficient can be increased
                        for i in range(m):
                            if c[i] > 1e-10:
                                return [1, None]  # Infinity
        except:
            continue
    
    return [0, best_solution]  # Bounded solution

def solve_system(equations, rhs, m):
    # Simple Gaussian elimination for square system
    n = len(equations)
    if n != m:
        return None
    
    # Create augmented matrix
    aug = []
    for i in range(n):
        row = equations[i][:] + [rhs[i]]
        aug.append(row)
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        pivot_row = i
        for j in range(i + 1, n):
            if abs(aug[j][i]) > abs(aug[pivot_row][i]):
                pivot_row = j
        
        if abs(aug[pivot_row][i]) < 1e-10:
            return None  # Singular system
        
        # Swap rows
        aug[i], aug[pivot_row] = aug[pivot_row], aug[i]
        
        # Eliminate column
        for j in range(i + 1, n):
            if abs(aug[j][i]) > 1e-10:
                factor = aug[j][i] / aug[i][i]
                for k in range(i, m + 1):
                    aug[j][k] -= factor * aug[i][k]
    
    # Back substitution
    solution = [0.0] * m
    for i in range(m - 1, -1, -1):
        if abs(aug[i][i]) < 1e-10:
            return None
        
        solution[i] = aug[i][m]
        for j in range(i + 1, m):
            solution[i] -= aug[i][j] * solution[j]
        solution[i] /= aug[i][i]
    
    return solution

def satisfies_all_constraints(solution, A, b, m):
    # Check if solution satisfies all constraints
    for i in range(len(A)):
        lhs = sum(A[i][j] * solution[j] for j in range(m))
        if lhs > b[i] + 1e-6:  # Allow small numerical error
            return False
    
    # Check non-negativity
    for j in range(m):
        if solution[j] < -1e-6:
            return False
    
    return True

n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
c = list(map(int, stdin.readline().split()))

anst, ansx = solve_diet_problem(n, m, A, b, c)

if anst == -1:
  print("No solution")
if anst == 0:  
  print("Bounded solution")
  print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
if anst == 1:
  print("Infinity")
    
