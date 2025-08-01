import sys, threading

sys.setrecursionlimit(10**6)
threading.stack_size(2**27)

class Node:
    def __init__(self, key, left, right):
        self.key = key
        self.left = left
        self.right = right

def in_order_traversal(node, result, tree):
    if node == -1:
        return
    in_order_traversal(tree[node].left, result, tree)
    result.append(tree[node].key)
    in_order_traversal(tree[node].right, result, tree)

def is_bst(tree):
    if not tree:
        return True
    
    in_order_result = []
    in_order_traversal(0, in_order_result, tree)
    
    for i in range(1, len(in_order_result)):
        if in_order_result[i] <= in_order_result[i-1]:
            return False
            
    return True

def main():
    n = int(sys.stdin.readline())
    if n == 0:
        print("CORRECT")
        return
        
    tree = [Node(0, 0, 0) for i in range(n)]
    for i in range(n):
        key, left, right = map(int, sys.stdin.readline().strip().split())
        tree[i] = Node(key, left, right)

    if is_bst(tree):
        print("CORRECT")
    else:
        print("INCORRECT")

threading.Thread(target=main).start()