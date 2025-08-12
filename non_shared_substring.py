# python3
import sys


def solve(p, q):
    # Brute force shortest substring in p not in q
    for length in range(1, len(p) + 1):
        for i in range(len(p) - length + 1):
            sub = p[i:i+length]
            if sub not in q:
                return sub
    return ""


if __name__ == '__main__':
    p = sys.stdin.readline().strip()
    q = sys.stdin.readline().strip()
    ans = solve(p, q)
    sys.stdout.write(ans + '\n')
