# python3

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)

def SelectPivotElement(a, used_rows, used_columns):
    # Select pivot element with partial pivoting for numerical stability
    pivot_element = Position(0, 0)
    
    # Find first unused row
    while pivot_element.row < len(a) and used_rows[pivot_element.row]:
        pivot_element.row += 1
    
    # Find first unused column in this row
    while pivot_element.column < len(a) and used_columns[pivot_element.column]:
        pivot_element.column += 1
    
    # Partial pivoting: find the largest absolute value in the current column
    max_val = abs(a[pivot_element.row][pivot_element.column])
    best_row = pivot_element.row
    
    for i in range(pivot_element.row + 1, len(a)):
        if not used_rows[i] and abs(a[i][pivot_element.column]) > max_val:
            max_val = abs(a[i][pivot_element.column])
            best_row = i
    
    pivot_element.row = best_row
    return pivot_element

def SwapLines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column;

def ProcessPivotElement(a, b, pivot_element):
    # Perform Gaussian elimination step
    pivot_row = pivot_element.row
    pivot_col = pivot_element.column
    pivot_val = a[pivot_row][pivot_col]
    
    # Normalize the pivot row
    if abs(pivot_val) > EPS:
        for j in range(len(a[pivot_row])):
            a[pivot_row][j] /= pivot_val
        b[pivot_row] /= pivot_val
    
    # Eliminate the pivot column from all other rows
    for i in range(len(a)):
        if i != pivot_row and abs(a[i][pivot_col]) > EPS:
            factor = a[i][pivot_col]
            for j in range(len(a[i])):
                a[i][j] -= factor * a[pivot_row][j]
            b[i] -= factor * b[pivot_row]

def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns)
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)

    return b

def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])

if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    PrintColumn(solution)
    exit(0)
