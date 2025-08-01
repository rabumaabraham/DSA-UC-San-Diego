import heapq

def main():
    num_threads, num_jobs = map(int, input().split())
    jobs = list(map(int, input().split()))

    result = []
    heap = [(0, i) for i in range(num_threads)]  # (finish_time, thread_id)
    heapq.heapify(heap)

    for job_time in jobs:
        finish_time, thread_id = heapq.heappop(heap)
        result.append((thread_id, finish_time))
        heapq.heappush(heap, (finish_time + job_time, thread_id))

    for thread_id, start_time in result:
        print(thread_id, start_time)

if __name__ == "__main__":
    main()
