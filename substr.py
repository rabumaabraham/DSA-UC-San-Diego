import sys

class Solver:
    def __init__(self, s):
        self.s = s
        self.m1 = 10**9 + 7
        self.m2 = 10**9 + 9
        self.x = 263
        self._precompute_hashes()

    def _precompute_hashes(self):
        n = len(self.s)
        self.h1 = [0] * (n + 1)
        self.h2 = [0] * (n + 1)
        self.x_p1 = [1] * (n + 1)
        self.x_p2 = [1] * (n + 1)
        for i in range(1, n + 1):
            self.h1[i] = (self.x * self.h1[i - 1] + ord(self.s[i - 1])) % self.m1
            self.h2[i] = (self.x * self.h2[i - 1] + ord(self.s[i - 1])) % self.m2
            self.x_p1[i] = (self.x_p1[i - 1] * self.x) % self.m1
            self.x_p2[i] = (self.x_p2[i - 1] * self.x) % self.m2

    def _hash(self, h, x_p, a, l, m):
        y = h[a + l] - (x_p[l] * h[a]) % m
        return (y + m) % m

    def ask(self, a, b, l):
        h1a = self._hash(self.h1, self.x_p1, a, l, self.m1)
        h1b = self._hash(self.h1, self.x_p1, b, l, self.m1)
        h2a = self._hash(self.h2, self.x_p2, a, l, self.m2)
        h2b = self._hash(self.h2, self.x_p2, b, l, self.m2)
        return h1a == h1b and h2a == h2b

def main():
    s = sys.stdin.readline().strip()
    solver = Solver(s)
    q = int(sys.stdin.readline())
    for _ in range(q):
        a, b, l = map(int, sys.stdin.readline().split())
        print("Yes" if solver.ask(a, b, l) else "No")

if __name__ == '__main__':
    main()
