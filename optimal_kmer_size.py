# python3
import sys
from collections import defaultdict


def build_kmers(k, reads):
    """Build all k-mers from reads"""
    kmers = set()
    for read in reads:
        for i in range(len(read) - k + 1):
            kmers.add(read[i:i+k])
    return kmers


def build_de_bruijn_graph(kmers):
    """Build de Bruijn graph from k-mers"""
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        graph[prefix].append(suffix)
        out_degree[prefix] += 1
        in_degree[suffix] += 1
    
    return graph, in_degree, out_degree


def has_eulerian_cycle(graph, in_degree, out_degree):
    """Check if the graph has an Eulerian cycle"""
    # All vertices must have in-degree = out-degree
    all_vertices = set(graph.keys()) | set(in_degree.keys())
    
    for vertex in all_vertices:
        if in_degree[vertex] != out_degree[vertex]:
            return False
    
    # Check if graph is connected (simplified)
    if not graph:
        return False
    
    # Start from any vertex and check connectivity
    start = next(iter(graph.keys()))
    visited = set()
    stack = [start]
    
    while stack:
        current = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                stack.append(neighbor)
    
    return len(visited) == len(all_vertices)


def main():
    reads = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            reads.append(line)
    
    if not reads:
        print(1)
        return
    
    read_length = len(reads[0])
    
    # Try k from read_length down to 2
    for k in range(read_length, 1, -1):
        kmers = build_kmers(k, reads)
        if len(kmers) < 2:
            continue
            
        graph, in_degree, out_degree = build_de_bruijn_graph(kmers)
        
        if has_eulerian_cycle(graph, in_degree, out_degree):
            print(k)
            return
    
    print(1)


if __name__ == "__main__":
    main()