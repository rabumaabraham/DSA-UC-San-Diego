# python3
import sys


def build_suffix_tree_from_sa_lcp(text, sa, lcp):
    n = len(text)
    # node attributes
    parent = [-1]   # parent[node]
    string_depth = [0]  # length of string from root to node
    edge_start = [-1]   # edge_start[node] (edge from parent to node)
    edge_end = [-1]     # edge_end[node] (exclusive)
    children = [{}]     # children[node] : map first char -> child node id

    edges_output = []  # edges (start, end) in creation order

    def create_node(p, depth, start, end):
        node_id = len(parent)
        parent.append(p)
        string_depth.append(depth)
        edge_start.append(start)
        edge_end.append(end)
        children.append({})
        return node_id

    def add_leaf(node, suffix):
        start = suffix + string_depth[node]
        leaf = create_node(node, n - suffix, start, n)
        children[node][text[start]] = leaf
        edges_output.append((start, n))
        return leaf

    def split_edge(node, start, offset):
        # find child to split (child edge begins with text[start])
        ch = text[start]
        child = children[node][ch]
        child_start = edge_start[child]
        child_end = edge_end[child]
        # create mid node
        mid = create_node(
            node, string_depth[node] + offset, child_start, child_start + offset)
        # reassign child edge
        children[node][text[child_start]] = mid
        children[mid][text[child_start + offset]] = child
        parent[child] = mid
        # update child edge start
        edge_start[child] = child_start + offset
        # record the new edge (parent->mid)
        edges_output.append((child_start, child_start + offset))
        return mid

    root = 0
    lcp_prev = 0
    cur_node = root
    for i in range(len(sa)):
        suffix = sa[i]
        # climb to node such that string_depth[node] <= lcp_prev
        while string_depth[cur_node] > lcp_prev:
            cur_node = parent[cur_node]
        if string_depth[cur_node] == lcp_prev:
            leaf = add_leaf(cur_node, suffix)
            cur_node = leaf
        else:
            # need to split edge on path to previous suffix
            start = sa[i-1] + string_depth[cur_node]
            offset = lcp_prev - string_depth[cur_node]
            mid = split_edge(cur_node, start, offset)
            leaf = add_leaf(mid, suffix)
            cur_node = leaf
        if i < len(lcp):
            lcp_prev = lcp[i]

    return edges_output


if __name__ == "__main__":
    data = sys.stdin.read().strip().splitlines()
    if not data:
        sys.exit(0)
    text = data[0].strip()
    sa = list(map(int, data[1].split()))
    lcp = list(map(int, data[2].split())) if len(
        data) > 2 and data[2].strip() else []
    edges = build_suffix_tree_from_sa_lcp(text, sa, lcp)
    print(text)
    for a, b in edges:
        print(a, b)
