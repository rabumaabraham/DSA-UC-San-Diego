import sys, threading

sys.setrecursionlimit(10**6)
threading.stack_size(2**27)

class Node:
    def __init__(self, char, parent, left, right):
        self.char = char
        self.parent = parent
        self.left = left
        self.right = right
        self.size = 1
        if self.left:
            self.size += self.left.size
        if self.right:
            self.size += self.right.size

def update_size(node):
    if not node:
        return
    node.size = 1 + (node.left.size if node.left else 0) + (node.right.size if node.right else 0)

def small_rotation(node):
    parent = node.parent
    if not parent:
        return
    grandparent = parent.parent
    if parent.left == node:
        m = node.right
        node.right = parent
        parent.parent = node
        parent.left = m
        if m:
            m.parent = parent
    else:
        m = node.left
        node.left = parent
        parent.parent = node
        parent.right = m
        if m:
            m.parent = parent
    
    update_size(parent)
    update_size(node)
    
    node.parent = grandparent
    if grandparent:
        if grandparent.left == parent:
            grandparent.left = node
        else:
            grandparent.right = node

def big_rotation(node):
    parent = node.parent
    grandparent = parent.parent
    if parent.left == node and grandparent.left == parent:
        small_rotation(parent)
        small_rotation(node)
    elif parent.right == node and grandparent.right == parent:
        small_rotation(parent)
        small_rotation(node)
    else:
        small_rotation(node)
        small_rotation(node)

def splay(root, node):
    while node.parent:
        parent = node.parent
        grandparent = parent.parent
        if not grandparent:
            small_rotation(node)
            break
        big_rotation(node)
    return node

def find_by_index(root, index):
    current = root
    while current:
        left_size = current.left.size if current.left else 0
        if index == left_size:
            return splay(root, current)
        elif index < left_size:
            current = current.left
        else:
            index -= left_size + 1
            current = current.right
    return None

def split(root, index):
    if index == 0:
        return None, root
    
    left = find_by_index(root, index - 1)
    if not left:
        return None, root
        
    right = left.right
    left.right = None
    if right:
        right.parent = None
    update_size(left)
    return left, right

def merge(left, right):
    if not left:
        return right
    if not right:
        return left
    
    node = right
    while node.left:
        node = node.left
    
    right = splay(right, node)
    right.left = left
    left.parent = right
    update_size(right)
    return right

def build_tree(s):
    if not s:
        return None
    
    nodes = [Node(c, None, None, None) for c in s]
    for i in range(len(s) - 1):
        nodes[i].right = nodes[i+1]
        nodes[i+1].parent = nodes[i]
        update_size(nodes[i])
    
    root = nodes[0]
    while root.right:
        root = root.right
    
    return splay(root, nodes[0])

def print_tree(root):
    if not root:
        return ""
    
    result = []
    
    def in_order(node):
        if not node:
            return
        in_order(node.left)
        result.append(node.char)
        in_order(node.right)
    
    in_order(root)
    return "".join(result)

def main():
    s = sys.stdin.readline().strip()
    q = int(sys.stdin.readline())
    root = build_tree(s)
    
    for _ in range(q):
        i, j, k = map(int, sys.stdin.readline().split())
        
        # Cut substring S[i..j]
        root, right = split(root, j + 1)
        left, middle = split(root, i)
        
        # Insert it after the k-th symbol of the remaining string
        root = merge(left, right)
        left_new, right_new = split(root, k)
        
        root = merge(left_new, middle)
        root = merge(root, right_new)

    print(print_tree(root))

threading.Thread(target=main).start()