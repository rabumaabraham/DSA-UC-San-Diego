from collections import deque


class Request:
    def __init__(self, arrival, process):
        self.arrival = arrival
        self.process = process


class Response:
    def __init__(self, dropped, start_time):
        self.dropped = dropped
        self.start_time = start_time


class Buffer:
    def __init__(self, size):
        self.size = size
        self.finish_times = deque()

    def process(self, request):
        while self.finish_times and self.finish_times[0] <= request.arrival:
            self.finish_times.popleft()
        if len(self.finish_times) >= self.size:
            return Response(True, -1)
        start_time = max(
            request.arrival, self.finish_times[-1] if self.finish_times else 0)
        self.finish_times.append(start_time + request.process)
        return Response(False, start_time)


def main():
    size, n = map(int, input().split())
    buffer = Buffer(size)
    requests = [Request(*map(int, input().split())) for _ in range(n)]
    responses = [buffer.process(r) for r in requests]
    for r in responses:
        print(-1 if r.dropped else r.start_time)


if __name__ == "__main__":
    main()
