# python3
class StockCharts:
    def read_data(self):
        n, k = map(int, input().split())
        stock_data = [list(map(int, input().split())) for i in range(n)]
        return stock_data

    def write_response(self, result):
        print(result)

    def min_charts(self, stock_data):
        # This problem reduces to minimum path cover in DAG
        # Minimum path cover = n - maximum matching in bipartite graph
        n = len(stock_data)
        if n <= 1:
            return n
        
        # Create bipartite graph where we can match stocks
        # that can be placed on the same chart
        def can_place_together(stock1, stock2):
            # Check if stock1 can be placed completely below stock2
            return all(stock1[i] < stock2[i] for i in range(len(stock1)))
        
        # Find maximum matching in bipartite graph
        def max_matching():
            # match[i] = j means stock i is matched to stock j (in right partition)
            match = [-1] * n
            
            def dfs(u, visited):
                for v in range(n):
                    if v not in visited and can_place_together(stock_data[u], stock_data[v]):
                        visited.add(v)
                        if match[v] == -1 or dfs(match[v], visited):
                            match[v] = u
                            return True
                return False
            
            result = 0
            for u in range(n):
                if dfs(u, set()):
                    result += 1
            
            return result
        
        # Minimum path cover = n - maximum matching
        return n - max_matching()

    def solve(self):
        stock_data = self.read_data()
        result = self.min_charts(stock_data)
        self.write_response(result)

if __name__ == '__main__':
    stock_charts = StockCharts()
    stock_charts.solve()
