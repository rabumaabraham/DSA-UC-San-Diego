# Uses python3
import sys


def build_trie(patterns):
    tree = {0: {}}
    node_id = 0
    for pattern in patterns:
        current_node = 0
        for char in pattern:
            if char not in tree[current_node]:
                node_id += 1
                tree[current_node][char] = node_id
                tree[node_id] = {}
            current_node = tree[current_node][char]
    return tree


if __name__ == '__main__':
    patterns = sys.stdin.read().split()[1:]
    tree = build_trie(patterns)
    for node in tree:
        for c in tree[node]:
            print("{}->{}:{}".format(node, tree[node][c], c))
