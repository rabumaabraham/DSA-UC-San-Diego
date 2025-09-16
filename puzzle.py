# python3
import sys
from itertools import permutations


def read_pieces():
    """Read puzzle pieces from input"""
    pieces = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            # Parse format (up,left,down,right)
            content = line[1:-1]  # Remove parentheses
            parts = [part.strip() for part in content.split(',')]
            pieces.append(parts)
    return pieces


def get_corner_pieces(pieces):
    """Find pieces that can be corners (two black edges)"""
    corners = []
    for i, piece in enumerate(pieces):
        black_count = piece.count('black')
        if black_count == 2:
            corners.append(i)
    return corners


def get_edge_pieces(pieces):
    """Find pieces that can be edges (one black edge)"""
    edges = []
    for i, piece in enumerate(pieces):
        black_count = piece.count('black')
        if black_count == 1:
            edges.append(i)
    return edges


def get_inner_pieces(pieces):
    """Find pieces that can be inner (no black edges)"""
    inners = []
    for i, piece in enumerate(pieces):
        black_count = piece.count('black')
        if black_count == 0:
            inners.append(i)
    return inners


def can_be_corner(piece, position):
    """Check if a piece can be placed at a corner position"""
    if position == (0, 0):  # Top-left
        return piece[0] == 'black' and piece[1] == 'black'
    elif position == (0, 4):  # Top-right
        return piece[0] == 'black' and piece[3] == 'black'
    elif position == (4, 0):  # Bottom-left
        return piece[2] == 'black' and piece[1] == 'black'
    elif position == (4, 4):  # Bottom-right
        return piece[2] == 'black' and piece[3] == 'black'
    return False


def can_be_edge(piece, position):
    """Check if a piece can be placed at an edge position"""
    row, col = position
    
    if row == 0:  # Top edge
        return piece[0] == 'black'
    elif row == 4:  # Bottom edge
        return piece[2] == 'black'
    elif col == 0:  # Left edge
        return piece[1] == 'black'
    elif col == 4:  # Right edge
        return piece[3] == 'black'
    
    return False


def solve_puzzle_efficient(pieces):
    """Solve the puzzle more efficiently by using constraints"""
    n = 5
    grid = [[-1 for _ in range(n)] for _ in range(n)]
    used = [False] * len(pieces)
    
    # Classify pieces
    corners = get_corner_pieces(pieces)
    edges = get_edge_pieces(pieces)
    inners = get_inner_pieces(pieces)
    
    def backtrack(pos):
        if pos == n * n:
            return True
        
        row = pos // n
        col = pos % n
        
        # Determine which pieces can be placed here
        candidate_pieces = []
        
        if (row == 0 and col == 0) or (row == 0 and col == 4) or \
           (row == 4 and col == 0) or (row == 4 and col == 4):
            # Corner position
            candidate_pieces = [i for i in corners if not used[i]]
        elif row == 0 or row == 4 or col == 0 or col == 4:
            # Edge position
            candidate_pieces = [i for i in edges if not used[i]]
        else:
            # Inner position
            candidate_pieces = [i for i in inners if not used[i]]
        
        for piece_idx in candidate_pieces:
            piece = pieces[piece_idx]
            
            # Check if piece fits constraints for this position
            if not is_valid_piece_placement(piece, row, col, grid, pieces):
                continue
            
            # Place the piece
            grid[row][col] = piece_idx
            used[piece_idx] = True
            
            if backtrack(pos + 1):
                return True
            
            # Backtrack
            used[piece_idx] = False
            grid[row][col] = -1
        
        return False
    
    backtrack(0)
    return grid


def is_valid_piece_placement(piece, row, col, grid, pieces):
    """Check if placing a piece at (row, col) is valid"""
    n = 5
    
    # Check top edge
    if row == 0:
        if piece[0] != 'black':
            return False
    elif grid[row-1][col] != -1:
        top_piece = pieces[grid[row-1][col]]
        if piece[0] != top_piece[2]:
            return False
    
    # Check left edge
    if col == 0:
        if piece[1] != 'black':
            return False
    elif grid[row][col-1] != -1:
        left_piece = pieces[grid[row][col-1]]
        if piece[1] != left_piece[3]:
            return False
    
    # Check bottom edge
    if row == n - 1:
        if piece[2] != 'black':
            return False
    elif grid[row+1][col] != -1:
        bottom_piece = pieces[grid[row+1][col]]
        if piece[2] != bottom_piece[0]:
            return False
    
    # Check right edge
    if col == n - 1:
        if piece[3] != 'black':
            return False
    elif grid[row][col+1] != -1:
        right_piece = pieces[grid[row][col+1]]
        if piece[3] != right_piece[1]:
            return False
    
    return True


def print_solution(grid, pieces, n):
    """Print the solution in the required format"""
    for i in range(n):
        row_pieces = []
        for j in range(n):
            piece = pieces[grid[i][j]]
            piece_str = f"({piece[0]},{piece[1]},{piece[2]},{piece[3]})"
            row_pieces.append(piece_str)
        print(';'.join(row_pieces))


def main():
    pieces = read_pieces()
    
    # Solve the puzzle
    solution = solve_puzzle_efficient(pieces)
    
    # Print the solution
    print_solution(solution, pieces, 5)


if __name__ == "__main__":
    main()