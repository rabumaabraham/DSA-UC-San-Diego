# python3
import sys
from collections import defaultdict


def read_input():
    """Read input data"""
    lines = sys.stdin.read().strip().split('\n')
    t = int(lines[0])
    reads = []
    
    for i in range(1, t + 1):
        line = lines[i].strip()
        if '|' in line:
            # Read pair
            parts = line.split('|')
            read1 = parts[0]
            read2 = parts[1]
            d = int(parts[2])
            reads.append((read1, read2, d))
        else:
            # Single read
            reads.append(line)
    
    return reads


def build_kmers(k, reads):
    """Build all k-mers from reads"""
    kmers = []
    for read in reads:
        if isinstance(read, tuple):
            # Read pair
            read1, read2, d = read
            for i in range(len(read1) - k + 1):
                kmers.append(read1[i:i+k])
            for i in range(len(read2) - k + 1):
                kmers.append(read2[i:i+k])
        else:
            # Single read
            for i in range(len(read) - k + 1):
                kmers.append(read[i:i+k])
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
            next_vertex = graph[current].pop(0)
            stack.append(next_vertex)
        else:
            path.append(stack.pop())
    
    return path[::-1]


def reconstruct_contigs(path, k):
    """Reconstruct contigs from Eulerian path"""
    if not path:
        return []
    
    contigs = []
    current_contig = path[0]
    
    for i in range(1, len(path)):
        if len(path[i]) >= k:
            current_contig += path[i][-1]
        else:
            # Start new contig
            if current_contig:
                contigs.append(current_contig)
            current_contig = path[i]
    
    if current_contig:
        contigs.append(current_contig)
    
    return contigs


def main():
    reads = read_input()
    
    # Use k=20 for assembly
    k = 20
    kmers = build_kmers(k, reads)
    
    if not kmers:
        return
    
    graph, in_degree, out_degree = build_de_bruijn_graph(kmers)
    
    # Find Eulerian path
    path = find_eulerian_path(graph, in_degree, out_degree)
    
    # Reconstruct contigs
    contigs = reconstruct_contigs(path, k)
    
    # Output in FASTA format
    for i, contig in enumerate(contigs):
        if len(contig) >= k:  # Only output contigs of reasonable length
            print(f">CONTIG{i+1}")
            print(contig)


if __name__ == "__main__":
    main()
