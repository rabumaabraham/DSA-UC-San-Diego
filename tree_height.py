import sys
import threading

def compute_height(n, parents):
    tree = [[] for _ in range(n)]
    root = -1
    for child_index in range(n):
        parent_index = parents[child_index]
        if parent_index == -1:
            root = child_index
        else:
            tree[parent_index].append(child_index)
    
    def dfs(node):
        if not tree[node]:
            return 1
        return 1 + max(dfs(child) for child in tree[node])
    
    return dfs(root)

def main():
    n = int(sys.stdin.readline())
    parents = list(map(int, sys.stdin.readline().split()))
    print(compute_height(n, parents))

threading.Thread(target=main).start()
