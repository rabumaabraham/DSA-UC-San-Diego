from collections import deque

def max_sliding_window(a, m):
    dq = deque()
    result = []

    for i in range(len(a)):
        while dq and dq[0] <= i - m:
            dq.popleft()
        while dq and a[dq[-1]] < a[i]:
            dq.pop()
        dq.append(i)
        if i >= m - 1:
            result.append(a[dq[0]])
    return result

def main():
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    print(*max_sliding_window(a, m))

if __name__ == "__main__":
    main()
