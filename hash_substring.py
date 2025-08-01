def hash_func(s, p, x):
    hash_val = 0
    for i in reversed(range(len(s))):
        hash_val = (hash_val * x + ord(s[i])) % p
    return hash_val

def precompute_hashes(text, pat_len, p, x):
    n = len(text)
    H = [0] * (n - pat_len + 1)
    S = text[n - pat_len:]
    H[-1] = hash_func(S, p, x)
    y = pow(x, pat_len, p)
    for i in reversed(range(n - pat_len)):
        H[i] = (x * H[i + 1] + ord(text[i]) - y * ord(text[i + pat_len])) % p
    return H

def main():
    pattern = input()
    text = input()
    p = 10**9 + 7
    x = 263
    p_hash = hash_func(pattern, p, x)
    hashes = precompute_hashes(text, len(pattern), p, x)
    result = [i for i in range(len(hashes)) if hashes[i] == p_hash and text[i:i+len(pattern)] == pattern]
    print(*result)

if __name__ == "__main__":
    main()
