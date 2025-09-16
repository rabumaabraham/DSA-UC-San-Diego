# python3
import sys
from collections import defaultdict
import itertools


def read_input():
    """Read input data"""
    data = sys.stdin.read().strip().split()
    k = int(data[0])
    t = int(data[1])
    reads = data[2:]
    return k, t, reads


def build_kmers(k, reads):
    """Build all k-mers from reads"""
    kmers = set()
    for read in reads:
        for i in range(len(read) - k + 1):
            kmers.add(read[i:i+k])
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


def find_disjoint_paths(graph, start, end, max_length):
    """Find all disjoint paths between start and end with length <= max_length"""
    paths = []
    
    def dfs(current, path, visited):
        if current == end and len(path) > 1:
            paths.append(path[:])
            return
        
        if len(path) > max_length:
            return
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                path.append(neighbor)
                visited.add(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)
    
    dfs(start, [start], {start})
    return paths


def paths_disjoint(path1, path2):
    """Check if two paths are disjoint (only share start and end)"""
    set1 = set(path1)
    set2 = set(path2)
    intersection = set1 & set2
    return len(intersection) == 2  # Only start and end vertices


def count_bubbles(graph, t):
    """Count the number of bubbles in the graph"""
    bubbles = 0
    paths_dict = defaultdict(list)
    
    # Find all vertices with multiple outgoing edges
    sources = [v for v, neighbors in graph.items() if len(neighbors) > 1]
    
    for source in sources:
        # Find all possible targets (vertices with multiple incoming edges)
        targets = [v for v in graph if v != source and len([u for u in graph if v in graph[u]]) > 1]
        
        for target in targets:
            # Find all paths from source to target
            paths = find_disjoint_paths(graph, source, target, t)
            
            if len(paths) >= 2:
                # Check all pairs of paths for disjointness
                for path1, path2 in itertools.combinations(paths, 2):
                    if paths_disjoint(path1, path2):
                        bubbles += 1
    
    return bubbles


def main():
    k, t, reads = read_input()
    kmers = build_kmers(k, reads)
    graph, in_degree = build_de_bruijn_graph(kmers)
    
    bubbles = count_bubbles(graph, t)
    print(bubbles)


if __name__ == "__main__":
    main()