import sys, threading

sys.setrecursionlimit(10**6)  # max depth of recursion
threading.stack_size(2**27)   # new thread will get stack of such size

class Node:
  def __init__(self, key, left, right):
    self.key = key
    self.left = left
    self.right = right

def in_order_recursive(node, result, tree):
    if node == -1:
        return
    in_order_recursive(tree[node].left, result, tree)
    result.append(tree[node].key)
    in_order_recursive(tree[node].right, result, tree)

def pre_order_recursive(node, result, tree):
    if node == -1:
        return
    result.append(tree[node].key)
    pre_order_recursive(tree[node].left, result, tree)
    pre_order_recursive(tree[node].right, result, tree)

def post_order_recursive(node, result, tree):
    if node == -1:
        return
    post_order_recursive(tree[node].left, result, tree)
    post_order_recursive(tree[node].right, result, tree)
    result.append(tree[node].key)

def main():
  n = int(sys.stdin.readline())
  if n == 0:
    print("")
    print("")
    print("")
    return
  tree = [Node(0, 0, 0) for i in range(n)]
  for i in range(n):
    key, left, right = map(int, sys.stdin.readline().strip().split())
    tree[i] = Node(key, left, right)

  in_order_result = []
  in_order_recursive(0, in_order_result, tree)
  print(*in_order_result)

  pre_order_result = []
  pre_order_recursive(0, pre_order_result, tree)
  print(*pre_order_result)

  post_order_result = []
  post_order_recursive(0, post_order_result, tree)
  print(*post_order_result)

threading.Thread(target=main).start()