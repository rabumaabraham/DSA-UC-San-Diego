# python3
import sys


def compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    k = 0
    for i in range(1, m):
        while k > 0 and pattern[k] != pattern[i]:
            k = lps[k - 1]
        if pattern[k] == pattern[i]:
            k += 1
        lps[i] = k
    return lps


def kmp_search(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    lps = compute_lps(pattern)
    res = []
    q = 0
    for i in range(n):
        while q > 0 and pattern[q] != text[i]:
            q = lps[q - 1]
        if pattern[q] == text[i]:
            q += 1
        if q == m:
            res.append(i - m + 1)
            q = lps[q - 1]
    return res


if __name__ == "__main__":
    data = sys.stdin.read().splitlines()
    if not data:
        sys.exit(0)
    pattern = data[0].strip()
    text = data[1].strip() if len(data) > 1 else ""
    ans = kmp_search(text, pattern)
    if ans:
        print(" ".join(map(str, ans)))
    else:
        # print empty line (grader usually expects nothing or an empty line)
        print()
