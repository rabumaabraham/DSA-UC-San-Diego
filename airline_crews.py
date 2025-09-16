# python3
class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        return adj_matrix

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, adj_matrix):
        # Implement maximum bipartite matching using DFS
        n = len(adj_matrix)
        m = len(adj_matrix[0])
        
        # match[crew] = flight means crew is matched to flight
        match = [-1] * m  # crew -> flight mapping
        
        def dfs(flight, visited_crews):
            # Try to find an augmenting path starting from this flight
            for crew in range(m):
                if adj_matrix[flight][crew] == 1 and crew not in visited_crews:
                    visited_crews.add(crew)
                    # If crew is not matched, or we can find an augmenting path
                    # through the currently matched flight of this crew
                    if match[crew] == -1 or dfs(match[crew], visited_crews):
                        match[crew] = flight
                        return True
            return False
        
        # Find maximum matching
        for flight in range(n):
            dfs(flight, set())
        
        # Convert crew->flight mapping to flight->crew mapping
        flight_to_crew = [-1] * n
        for crew in range(m):
            if match[crew] != -1:
                flight_to_crew[match[crew]] = crew
        
        return flight_to_crew

    def solve(self):
        adj_matrix = self.read_data()
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)

if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()
