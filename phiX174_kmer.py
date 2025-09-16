# python3
import sys
from collections import defaultdict


def read_kmers():
    """Read k-mers from input"""
    kmers = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            kmers.append(line)
    return kmers


def build_de_bruijn_graph(kmers):
    """Build de Bruijn graph from k-mers"""
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for kmer in kmers:
        prefix = kmer[:-1]  # (k-1)-mer prefix
        suffix = kmer[1:]   # (k-1)-mer suffix
        graph[prefix].append(suffix)
        out_degree[prefix] += 1
        in_degree[suffix] += 1
    
    return graph, in_degree, out_degree


def find_eulerian_path(graph, in_degree, out_degree):
    """Find Eulerian path in the de Bruijn graph"""
    # Find start vertex (out-degree > in-degree)
    start = None
    for vertex in graph:
        if out_degree[vertex] > in_degree[vertex]:
            start = vertex
            break
    
    # If no start found, use any vertex with outgoing edges
    if start is None:
        for vertex in graph:
            if graph[vertex]:
                start = vertex
                break
    
    if start is None:
        return []
    
    # Find Eulerian path using Hierholzer's algorithm
    stack = [start]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            # Follow an edge
            next_vertex = graph[current].pop(0)
            stack.append(next_vertex)
        else:
            # Backtrack
            path.append(stack.pop())
    
    return path[::-1]  # Reverse to get the correct order


def reconstruct_genome(path, k):
    """Reconstruct genome from Eulerian path"""
    if not path:
        return ""
    
    result = path[0]
    for i in range(1, len(path)):
        result += path[i][-1]
    
    return result


def main():
    kmers = read_kmers()
    
    if not kmers:
        print("")
        return
    
    k = len(kmers[0])
    graph, in_degree, out_degree = build_de_bruijn_graph(kmers)
    
    # Find Eulerian path
    path = find_eulerian_path(graph, in_degree, out_degree)
    
    # Reconstruct genome
    genome = reconstruct_genome(path, k)
    
    # For circular genome, remove the last (k-1) characters to avoid duplication
    if len(genome) > k - 1:
        genome = genome[:-(k-1)]
    
    print(genome)


if __name__ == "__main__":
    main()