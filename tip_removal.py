# python3
import sys
from collections import defaultdict


def read_input():
    """Read input data"""
    reads = sys.stdin.read().strip().split()
    return reads


def build_kmers(k, reads):
    """Build all k-mers from reads"""
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


def remove_tips(graph, in_degree, max_length=15):
    """Remove tips from the de Bruijn graph"""
    edges_removed = 0
    changed = True
    
    while changed:
        changed = False
        
        # Find tips to remove
        tips_to_remove = []
        
        for vertex, neighbors in graph.items():
            if len(neighbors) == 1 and in_degree[vertex] == 0:
                # This is a tip (no incoming edges, one outgoing edge)
                tips_to_remove.append(vertex)
            elif len(neighbors) > 1:
                # Check outgoing tips
                for neighbor in list(neighbors):
                    if is_outgoing_tip(graph, in_degree, vertex, neighbor, max_length):
                        tips_to_remove.append((vertex, neighbor))
        
        # Remove tips
        for tip in tips_to_remove:
            if isinstance(tip, tuple):
                # Remove outgoing tip
                vertex, neighbor = tip
                graph[vertex].remove(neighbor)
                in_degree[neighbor] -= 1
                edges_removed += 1
                changed = True
            else:
                # Remove incoming tip
                vertex = tip
                if vertex in graph and graph[vertex]:
                    neighbor = next(iter(graph[vertex]))
                    graph[vertex].remove(neighbor)
                    in_degree[neighbor] -= 1
                    edges_removed += 1
                    changed = True
    
    return edges_removed


def is_outgoing_tip(graph, in_degree, start, neighbor, max_length):
    """Check if a path starting from start->neighbor is a tip"""
    current = neighbor
    path_length = 1
    
    while path_length < max_length:
        if current not in graph or len(graph[current]) == 0:
            # Dead end - this is a tip
            return True
        
        if len(graph[current]) > 1 or in_degree[current] > 1:
            # Junction or multiple incoming edges - not a tip
            return False
        
        # Continue along the path
        current = next(iter(graph[current]))
        path_length += 1
    
    return False


def main():
    reads = read_input()
    k = 15
    kmers = build_kmers(k, reads)
    graph, in_degree = build_de_bruijn_graph(kmers)
    
    edges_removed = remove_tips(graph, in_degree)
    print(edges_removed)


if __name__ == "__main__":
    main()