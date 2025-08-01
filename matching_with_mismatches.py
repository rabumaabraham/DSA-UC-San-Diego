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

def get_hash(s, p, x):
    n = len(s)
    H = [0] * (n + 1)
    for i in range(1, n + 1):
        H[i] = (x * H[i - 1] + ord(s[i - 1])) % p
    return H

def substring_hash(H, x_pows, start, length, p):
    y = (H[start + length] - x_pows[length] * H[start]) % p
    return (y + p) % p

def mismatch_index(pattern, text, p, x, x_pows, H_p, H_t, start):
    l, r = 0, len(pattern) - 1
    while l <= r:
        m = (l + r) // 2
        hash_p = substring_hash(H_p, x_pows, 0, m + 1, p)
        hash_t = substring_hash(H_t, x_pows, start, m + 1, p)
        if hash_p == hash_t:
            l = m + 1
        else:
            r = m - 1
    return l  # first mismatch position

def main():
    p = 10**9 + 7
    x = 263

    pattern = input().strip()
    text = input().strip()

    m, n = len(pattern), len(text)

    result = []
    if m > n:
        print()
        return

    x_pows = [1] * (max(m, n) + 1)
    for i in range(1, len(x_pows)):
        x_pows[i] = (x_pows[i - 1] * x) % p

    H_pattern = get_hash(pattern, p, x)
    H_text = get_hash(text, p, x)

    full_hash_p = substring_hash(H_pattern, x_pows, 0, m, p)

    for i in range(n - m + 1):
        hash_t = substring_hash(H_text, x_pows, i, m, p)
        if hash_t == full_hash_p:
            result.append(i)
        else:
            mismatch = mismatch_index(pattern, text, p, x, x_pows, H_pattern, H_text, i)
            if mismatch < m:
                hash_p2 = substring_hash(H_pattern, x_pows, mismatch + 1, m - mismatch - 1, p)
                hash_t2 = substring_hash(H_text, x_pows, i + mismatch + 1, m - mismatch - 1, p)
                if hash_p2 == hash_t2:
                    result.append(i)

    print(*result)

if __name__ == "__main__":
    main()
