class QueryProcessor:
    def __init__(self, m):
        self.m = m
        self.multiplier = 263
        self.prime = 10**9 + 7
        self.table = [[] for _ in range(m)]

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            ans = (ans * self.multiplier + ord(c)) % self.prime
        return ans % self.m

    def process_query(self, query):
        if query[0] == "add":
            ind = self._hash_func(query[1])
            if query[1] not in self.table[ind]:
                self.table[ind].insert(0, query[1])
        elif query[0] == "del":
            ind = self._hash_func(query[1])
            if query[1] in self.table[ind]:
                self.table[ind].remove(query[1])
        elif query[0] == "find":
            ind = self._hash_func(query[1])
            print("yes" if query[1] in self.table[ind] else "no")
        elif query[0] == "check":
            ind = int(query[1])
            print(" ".join(self.table[ind]))

def main():
    m = int(input())
    n = int(input())
    processor = QueryProcessor(m)
    for _ in range(n):
        query = input().split()
        processor.process_query(query)

if __name__ == "__main__":
    main()
