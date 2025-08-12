# python3
import sys


def sort_characters(s):
    n = len(s)
    alphabet = sorted(set(s))
    char_to_idx = {c: i for i, c in enumerate(alphabet)}
    count = [0] * len(alphabet)
    for ch in s:
        count[char_to_idx[ch]] += 1
    pos = [0] * len(alphabet)
    for i in range(1, len(alphabet)):
        pos[i] = pos[i-1] + count[i-1]
    order = [0] * n
    for i in range(n):
        cidx = char_to_idx[s[i]]
        order[pos[cidx]] = i
        pos[cidx] += 1
    return order, char_to_idx


def compute_char_classes(s, order):
    n = len(s)
    cl = [0] * n
    cl[order[0]] = 0
    for i in range(1, n):
        if s[order[i]] != s[order[i-1]]:
            cl[order[i]] = cl[order[i-1]] + 1
        else:
            cl[order[i]] = cl[order[i-1]]
    return cl


def sort_doubled(s, L, order, cl):
    n = len(s)
    count = [0] * n
    for i in range(n):
        count[cl[i]] += 1
    pos = [0] * n
    for i in range(1, n):
        pos[i] = pos[i-1] + count[i-1]
    new_order = [0] * n
    for i in range(n):
        start = (order[i] - L) % n
        cl_num = cl[start]
        new_order[pos[cl_num]] = start
        pos[cl_num] += 1
    return new_order


def update_classes(new_order, cl, L):
    n = len(new_order)
    new_cl = [0] * n
    new_cl[new_order[0]] = 0
    for i in range(1, n):
        cur, prev = new_order[i], new_order[i-1]
        mid, mid_prev = (cur + L) % n, (prev + L) % n
        if cl[cur] != cl[prev] or cl[mid] != cl[mid_prev]:
            new_cl[cur] = new_cl[prev] + 1
        else:
            new_cl[cur] = new_cl[prev]
    return new_cl


def build_suffix_array(s):
    order, _ = sort_characters(s)
    cl = compute_char_classes(s, order)
    L = 1
    n = len(s)
    while L < n:
        order = sort_doubled(s, L, order, cl)
        cl = update_classes(order, cl, L)
        L *= 2
    return order


if __name__ == "__main__":
    text = sys.stdin.readline().strip()
    sa = build_suffix_array(text)
    print(" ".join(map(str, sa)))
