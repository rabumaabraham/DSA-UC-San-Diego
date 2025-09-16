# python3
import sys
from collections import deque


class FlowGraph:
    def __init__(self, n):
        self.n = n
        self.edges = []
        self.graph = [[] for _ in range(n)]
    
    def add_edge(self, u, v, capacity):
        self.graph[u].append(len(self.edges))
        self.edges.append([u, v, capacity])
        
        self.graph[v].append(len(self.edges))
        self.edges.append([v, u, 0])
    
    def size(self):
        return self.n
    
    def get_ids(self, u):
        return self.graph[u]
    
    def get_edge(self, id):
        return self.edges[id]
    
    def add_flow(self, id, flow):
        self.edges[id][2] -= flow
        self.edges[id ^ 1][2] += flow


def max_flow(graph, from_, to):
    """Find maximum flow using Edmonds-Karp algorithm"""
    flow = 0
    while True:
        # BFS to find augmenting path
        queue = deque([from_])
        parent = [-1] * graph.size()
        parent[from_] = from_
        
        while queue:
            u = queue.popleft()
            for edge_id in graph.get_ids(u):
                edge = graph.get_edge(edge_id)
                if parent[edge[1]] == -1 and edge[2] > 0:
                    parent[edge[1]] = edge_id
                    if edge[1] == to:
                        break
                    queue.append(edge[1])
        
        if parent[to] == -1:
            break
        
        # Find bottleneck capacity
        path_flow = float('inf')
        v = to
        while v != from_:
            edge_id = parent[v]
            edge = graph.get_edge(edge_id)
            path_flow = min(path_flow, edge[2])
            v = edge[0]
        
        # Update flow
        v = to
        while v != from_:
            edge_id = parent[v]
            graph.add_flow(edge_id, path_flow)
            v = graph.get_edge(edge_id)[0]
        
        flow += path_flow
    
    return flow


def solve_circulation(n, m, edges):
    """Solve circulation problem by reducing to max flow"""
    # Create a new graph with source and sink
    # Add source (n) and sink (n+1)
    source = n
    sink = n + 1
    
    # Calculate required flow for each vertex
    required_flow = [0] * n
    for u, v, lower, upper in edges:
        required_flow[u] -= lower  # Outgoing lower bound
        required_flow[v] += lower  # Incoming lower bound
    
    # Create flow graph
    flow_graph = FlowGraph(n + 2)
    
    # Add edges with modified capacities
    for u, v, lower, upper in edges:
        flow_graph.add_edge(u, v, upper - lower)
    
    # Add edges from source to vertices with positive required flow
    # Add edges from vertices with negative required flow to sink
    total_source_flow = 0
    for i in range(n):
        if required_flow[i] > 0:
            flow_graph.add_edge(source, i, required_flow[i])
            total_source_flow += required_flow[i]
        elif required_flow[i] < 0:
            flow_graph.add_edge(i, sink, -required_flow[i])
    
    # Find maximum flow
    max_flow_value = max_flow(flow_graph, source, sink)
    
    # Check if all required flow is satisfied
    if max_flow_value != total_source_flow:
        return None  # No circulation exists
    
    # Extract the actual flow values by examining the flow graph
    flow_values = []
    for i, (u, v, lower, upper) in enumerate(edges):
        # Find the edge in the flow graph (it's the 2*i-th edge)
        edge_id = 2 * i
        edge = flow_graph.get_edge(edge_id)
        actual_flow = upper - edge[2]  # Original capacity - remaining capacity
        flow_values.append(actual_flow)
    
    return flow_values


def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    m = data[1]
    
    edges = []
    for i in range(m):
        u = data[2 + 4*i] - 1  # Convert to 0-indexed
        v = data[3 + 4*i] - 1
        lower = data[4 + 4*i]
        upper = data[5 + 4*i]
        edges.append((u, v, lower, upper))
    
    result = solve_circulation(n, m, edges)
    
    if result is None:
        print("NO")
    else:
        print("YES")
        for flow in result:
            print(flow)


if __name__ == "__main__":
    main()