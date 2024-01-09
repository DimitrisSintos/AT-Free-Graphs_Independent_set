from graph import Graph

class BruteForce:
    def __init__(self, graph: Graph):
        self.graph = graph
        
    def is_independent_set(self, vertices_set):
        for vertex in vertices_set:
            for neighbor in self.graph.adjacency_list[vertex]:
                if neighbor in vertices_set:
                    return False
        return True

    def maximum_independent_set_size(self):
        max_size = 0
        for i in range(1, 2 ** self.graph.num_of_vertices):
            subset = set()
            for j in range(self.graph.num_of_vertices):
                if i & (1 << j):
                    subset.add(str(j))
            if self.is_independent_set(subset):
                max_size = max(max_size, len(subset))
        return max_size
    
    def run(self):
        return self.maximum_independent_set_size()