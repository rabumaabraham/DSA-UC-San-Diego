def poly_hash(s, p, x):
    hash_val = 0
    for c in reversed(s):
        hash_val = (hash_val * x + ord(c)) % p
    return hash_val

def precompute_hashes(s, l, p, x):
    n = len(s)
    H = [0] * (n - l + 1)
    S = s[n - l:]
    H[-1] = poly_hash(S, p, x)
    y = pow(x, l, p)
    for i in reversed(range(n - l)):
        H[i] = (x * H[i + 1] + ord(s[i]) - y * ord(s[i + l])) % p
    return H

def check(s1, s2, l, p, x):
    hashes = {}
    h1 = precompute_hashes(s1, l, p, x)
    for i in range(len(h1)):
        hashes[h1[i]] = i
    h2 = precompute_hashes(s2, l, p, x)
    for j in range(len(h2)):
        if h2[j] in hashes:
            return (hashes[h2[j]], j)
    return None

def longest_common_substring(s1, s2):
    p = 10**9 + 7
    x = 263
    left, right = 0, min(len(s1), len(s2))
    answer = (0, 0, 0)
    while left <= right:
        mid = (left + right) // 2
        res = check(s1, s2, mid, p, x)
        if res:
            answer = (res[0], res[1], mid)
            left = mid + 1
        else:
            right = mid - 1
    return answer

def main():
    s1 = input()
    s2 = input()
    i, j, l = longest_common_substring(s1, s2)
    print(i, j, l)

if __name__ == "__main__":
    main()
