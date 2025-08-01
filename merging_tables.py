def main():
    n, m = map(int, input().split())
    sizes = list(map(int, input().split()))
    parents = list(range(n))
    ranks = [0] * n
    max_size = max(sizes)

    def find(i):
        if i != parents[i]:
            parents[i] = find(parents[i])
        return parents[i]

    def union(destination, source):
        nonlocal max_size
        real_dest = find(destination)
        real_source = find(source)
        if real_dest == real_source:
            return
        if ranks[real_dest] < ranks[real_source]:
            real_dest, real_source = real_source, real_dest
        parents[real_source] = real_dest
        if ranks[real_dest] == ranks[real_source]:
            ranks[real_dest] += 1
        sizes[real_dest] += sizes[real_source]
        sizes[real_source] = 0
        max_size = max(max_size, sizes[real_dest])

    for _ in range(m):
        dst, src = map(int, input().split())
        union(dst - 1, src - 1)
        print(max_size)

if __name__ == "__main__":
    main()
