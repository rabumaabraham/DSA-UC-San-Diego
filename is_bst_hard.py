import sys, threading

sys.setrecursionlimit(10**6)
threading.stack_size(2**27)

class Node:
    def __init__(self, key, left, right):
        self.key = key
        self.left = left
        self.right = right

def is_bst_hard_recursive(node_idx, tree, min_val, max_val):
    if node_idx == -1:
        return True
    
    node = tree[node_idx]
    
    if node.key < min_val or node.key >= max_val:
        return False
        
    if not is_bst_hard_recursive(node.left, tree, min_val, node.key):
        return False
        
    if not is_bst_hard_recursive(node.right, tree, node.key, max_val):
        return False
        
    return True

def is_bst_hard(tree):
    if not tree:
        return True

    return is_bst_hard_recursive(0, tree, -float('inf'), float('inf'))

def main():
    n = int(sys.stdin.readline())
    if n == 0:
        print("CORRECT")
        return
    
    tree = [Node(0, 0, 0) for i in range(n)]
    for i in range(n):
        key, left, right = map(int, sys.stdin.readline().strip().split())
        tree[i] = Node(key, left, right)

    if is_bst_hard(tree):
        print("CORRECT")
    else:
        print("INCORRECT")

threading.Thread(target=main).start()