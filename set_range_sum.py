import sys, threading

sys.setrecursionlimit(10**6)
threading.stack_size(2**27)

class Node:
    def __init__(self, key, sum, left, right, parent):
        self.key = key
        self.sum = sum
        self.left = left
        self.right = right
        self.parent = parent

def update_sum(node):
    if not node:
        return
    node.sum = node.key + (node.left.sum if node.left else 0) + (node.right.sum if node.right else 0)

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
    
    update_sum(parent)
    update_sum(node)
    
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

def find(root, key):
    node = root
    last = root
    next_node = None
    while node:
        last = node
        if node.key >= key and (not next_node or node.key < next_node.key):
            next_node = node
        if key == node.key:
            break
        if key < node.key:
            node = node.left
        else:
            node = node.right
    
    if last:
        root = splay(root, last)
    return next_node, root

def split(root, key):
    result, root = find(root, key)
    if not result:
        return root, None
    
    right = splay(root, result)
    left = right.left
    right.left = None
    if left:
        left.parent = None
    update_sum(right)
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
    update_sum(right)
    return right

def add(root, key):
    if not root:
        return Node(key, key, None, None, None)
    
    left, right = split(root, key)
    
    if right and right.key == key:
        return merge(left, right)
    
    new_node = Node(key, key, None, None, None)
    new_node.left = left
    if left:
        left.parent = new_node
    new_node.right = right
    if right:
        right.parent = new_node
    update_sum(new_node)
    return new_node

def delete(root, key):
    if not root:
        return None
    
    result, root = find(root, key)
    if not result or result.key != key:
        return root
    
    splay_node = splay(root, result)
    left = splay_node.left
    right = splay_node.right
    
    if left:
        left.parent = None
    if right:
        right.parent = None

    splay_node.left = splay_node.right = None
    
    return merge(left, right)

def range_sum(root, l, r):
    left, middle = split(root, l)
    middle, right = split(middle, r + 1)
    
    result = middle.sum if middle else 0
    
    root = merge(left, middle)
    root = merge(root, right)
    
    return result, root

def main():
    MOD = 1000000001
    root = None
    x = 0
    n = int(sys.stdin.readline())
    
    for _ in range(n):
        line = sys.stdin.readline().split()
        op = line[0]
        
        if op == '+':
            i = int(line[1])
            root = add(root, (i + x) % MOD)
        elif op == '-':
            i = int(line[1])
            root = delete(root, (i + x) % MOD)
        elif op == '?':
            i = int(line[1])
            key = (i + x) % MOD
            result, root = find(root, key)
            if result and result.key == key:
                print("Found")
            else:
                print("Not found")
        elif op == 's':
            l, r = map(int, line[1:])
            l = (l + x) % MOD
            r = (r + x) % MOD
            
            x, root = range_sum(root, l, r)
            print(x)

threading.Thread(target=main).start()