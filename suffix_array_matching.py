# python3
import sys


def build_suffix_array(s):
    # reuse the doubling algorithm from suffix_array_long but condensed for reuse
    n = len(s)
    order = sort_characters_local(s)
    cl = compute_char_classes_local(s, order)
    L = 1
    while L < n:
        order = sort_doubled_local(s, L, order, cl)
        cl = update_classes_local(order, cl, L)
        L *= 2
    return order


def sort_characters_local(s):
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
    return order


def compute_char_classes_local(s, order):
    n = len(s)
    cl = [0] * n
    for i in range(1, n):
        cl[order[i]] = cl[order[i-1]] + (s[order[i]] != s[order[i-1]])
    return cl


def sort_doubled_local(s, L, order, cl):
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
        c = cl[start]
        new_order[pos[c]] = start
        pos[c] += 1
    return new_order


def update_classes_local(new_order, cl, L):
    n = len(new_order)
    new_cl = [0] * n
    for i in range(1, n):
        cur, prev = new_order[i], new_order[i-1]
        mid, mid_prev = (cur + L) % n, (prev + L) % n
        new_cl[cur] = new_cl[prev] + \
            (cl[cur] != cl[prev] or cl[mid] != cl[mid_prev])
    return new_cl


def find_occurrences(text, patterns):
    n = len(text)
    sa = build_suffix_array(text)
    res_positions = set()

    def cmp_sub(i, pattern):
        # compare text suffix starting at i with pattern lexicographically up to len(pattern)
        sub = text[i:i+len(pattern)]
        if sub == pattern:
            return 0
        return -1 if sub < pattern else 1

    def lower_bound(pattern):
        left, right = 0, n
        while left < right:
            mid = (left + right) // 2
            if text[sa[mid]:sa[mid]+len(pattern)] < pattern:
                left = mid + 1
            else:
                right = mid
        return left

    def upper_bound(pattern):
        left, right = 0, n
        while left < right:
            mid = (left + right) // 2
            if text[sa[mid]:sa[mid]+len(pattern)] <= pattern:
                left = mid + 1
            else:
                right = mid
        return left

    for pat in patterns:
        if pat == "":
            continue
        l = lower_bound(pat)
        r = upper_bound(pat)
        for i in range(l, r):
            # verify prefix match (since slices shorter than pat may compare)
            if text.startswith(pat, sa[i]):
                res_positions.add(sa[i])
    return res_positions


if __name__ == "__main__":
    data = sys.stdin.read().split()
    if not data:
        sys.exit(0)
    text = data[0].strip()
    if len(data) == 1:
        print()
        sys.exit(0)
    n = int(data[1])
    patterns = data[2:2 + n]
    positions = find_occurrences(text, patterns)
    if positions:
        print(" ".join(map(str, sorted(positions))))
    else:
        # If none, print empty line as per common grader expectations
        print()
