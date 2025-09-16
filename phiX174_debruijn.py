# python3
import sys
from collections import defaultdict


def read_reads():
    """Read sequencing reads from input"""
    reads = []
    for line in sys.stdin:
        read = line.strip()
        if read:
            reads.append(read)
    return reads


def build_kmers(k, reads):
    """Break reads into k-mers"""
    kmers = []
    for read in reads:
        for i in range(len(read) - k + 1):
            kmers.append(read[i:i+k])
    return kmers


def build_de_bruijn_graph(kmers):
    """Build de Bruijn graph from k-mers"""
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    
    for kmer in kmers:
        prefix = kmer[:-1]
        suffix = kmer[1:]
        if prefix != suffix:
            if suffix not in graph[prefix]:
                graph[prefix].add(suffix)
                in_degree[suffix] += 1
    
    return graph, in_degree


def remove_simple_tips(graph, in_degree, max_tip_length=15):
    """Remove simple tips from the de Bruijn graph"""
    edges_removed = 0
    changed = True
    
    while changed:
        changed = False
        
        # Find vertices with no incoming edges and one outgoing edge
        tips = []
        for vertex, neighbors in graph.items():
            if len(neighbors) == 1 and in_degree[vertex] == 0:
                tips.append(vertex)
        
        # Remove tips
        for tip in tips:
            if tip in graph and graph[tip]:
                neighbor = next(iter(graph[tip]))
                graph[tip].remove(neighbor)
                in_degree[neighbor] -= 1
                edges_removed += 1
                changed = True
        
        # Remove dead ends
        dead_ends = [v for v in graph if len(graph[v]) == 0]
        for dead_end in dead_ends:
            del graph[dead_end]
    
    return edges_removed


def find_eulerian_path(graph, in_degree):
    """Find Eulerian path in the de Bruijn graph"""
    if not graph:
        return []
    
    # Find start vertex (out-degree > in-degree)
    start = None
    for vertex in graph:
        if len(graph[vertex]) > in_degree[vertex]:
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
    
    # Find Eulerian path using stack-based approach
    stack = [start]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            neighbor = next(iter(graph[current]))
            graph[current].remove(neighbor)
            stack.append(neighbor)
        else:
            path.append(stack.pop())
    
    return path[::-1]


def reconstruct_genome(path, k):
    """Reconstruct genome from Eulerian path"""
    if not path:
        return ""
    
    # Start with the first vertex
    genome = path[0]
    
    # Add the last character of each subsequent vertex
    for i in range(1, len(path)):
        if len(path[i]) >= k - 1:
            genome += path[i][-1]
    
    return genome


def main():
    reads = read_reads()
    
    if not reads:
        print("")
        return
    
    # Use k=15 for assembly
    k = 15
    kmers = build_kmers(k, reads)
    
    if not kmers:
        print("")
        return
    
    # Build de Bruijn graph
    graph, in_degree = build_de_bruijn_graph(kmers)
    
    # Remove simple tips
    remove_simple_tips(graph, in_degree)
    
    # Find Eulerian path
    path = find_eulerian_path(graph, in_degree)
    
    # Reconstruct genome
    genome = reconstruct_genome(path, k)
    
    print(genome)


if __name__ == "__main__":
    main()