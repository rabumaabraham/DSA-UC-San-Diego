#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []


def ReadTree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree


def dfs(tree, vertex, parent):
    # For each vertex, compute two values:
    # include[vertex] = max weight if we include this vertex
    # exclude[vertex] = max weight if we exclude this vertex
    
    include = tree[vertex].weight  # Include current vertex
    exclude = 0                    # Exclude current vertex
    
    for child in tree[vertex].children:
        if child != parent:
            child_include, child_exclude = dfs(tree, child, vertex)
            
            # If we include current vertex, we must exclude all children
            include += child_exclude
            
            # If we exclude current vertex, we can choose best for each child
            exclude += max(child_include, child_exclude)
    
    return include, exclude


def MaxWeightIndependentTreeSubset(tree):
    size = len(tree)
    if size == 0:
        return 0
    
    include, exclude = dfs(tree, 0, -1)
    return max(include, exclude)


def main():
    tree = ReadTree();
    weight = MaxWeightIndependentTreeSubset(tree);
    print(weight)


# This is to avoid stack overflow issues
threading.Thread(target=main).start()
