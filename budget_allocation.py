# python3
from sys import stdin

n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))

def printEquisatisfiableSatFormula():
    # Convert ILP constraints Ax <= b to SAT formula
    # Each constraint sum(A[i][j] * x[j]) <= b[i] where x[j] ∈ {0,1}
    # is equivalent to: sum of positive coefficients + sum of negative coefficients <= b[i]
    
    clauses = []
    num_vars = m
    
    # Process each constraint
    for i in range(n):
        # Get positive and negative coefficients
        positive_vars = []
        negative_vars = []
        positive_sum = 0
        negative_sum = 0
        
        for j in range(m):
            if A[i][j] > 0:
                positive_vars.append((j + 1, A[i][j]))  # Variable indices start from 1
                positive_sum += A[i][j]
            elif A[i][j] < 0:
                negative_vars.append((j + 1, A[i][j]))
                negative_sum += A[i][j]
        
        # If positive_sum <= b[i], constraint is always satisfied
        if positive_sum <= b[i]:
            continue
            
        # If negative_sum > b[i], constraint is never satisfied
        if negative_sum > b[i]:
            # Add an unsatisfiable clause
            clauses.append([1, -1, 0])
            break
        
        # Generate clauses for this constraint
        # We need to ensure that if we select positive variables, 
        # we must also select enough negative variables to satisfy the constraint
        
        # For each subset of positive variables that violates the constraint,
        # we need at least one negative variable to be selected
        
        constraint_clauses = generate_constraint_clauses(positive_vars, negative_vars, b[i], m)
        clauses.extend(constraint_clauses)
    
    # If no constraints, add a trivial satisfiable clause
    if not clauses:
        clauses.append([1, 0])
    
    # Print SAT formula in DIMACS format
    print("{} {}".format(len(clauses), num_vars))
    for clause in clauses:
        print(" ".join(map(str, clause)))

def generate_constraint_clauses(positive_vars, negative_vars, b_val, num_vars):
    clauses = []
    
    if not positive_vars:
        return clauses
    
    # For each positive variable, if it's selected (True),
    # then at least one negative variable must be selected to balance
    for pos_var, pos_coeff in positive_vars:
        if pos_coeff > b_val:
            # This variable alone violates the constraint
            # So we need at least one negative variable
            if negative_vars:
                clause = [-pos_var]  # If pos_var is False, we're good
                for neg_var, neg_coeff in negative_vars:
                    clause.append(neg_var)  # At least one neg_var must be True
                clause.append(0)
                clauses.append(clause)
            else:
                # No negative variables to balance, so pos_var must be False
                clauses.append([-pos_var, 0])
    
    return clauses

printEquisatisfiableSatFormula()
