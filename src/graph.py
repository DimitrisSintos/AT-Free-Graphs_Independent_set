from itertools import combinations
from pyvis.network import Network
from component import Component
from interval import Interval


class Graph:
    show_count = 0  # Class-level variable to keep track of show calls

    def __init__(self, num_of_vertices, num_of_edges, edges, vertices=None):
        self.num_of_vertices = num_of_vertices
        self.num_of_edges = num_of_edges
        self.vertices = set(str(i) for i in range(num_of_vertices)) if vertices is None else vertices
        self.edges = set((str(u), str(v)) for u, v in edges)
        self.adjacency_list = {str(vertex): set() for vertex in self.vertices}
        for edge in self.edges:
            u, v = edge
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)
            
    
    def compute_all_components(self):
        components = {}
        for vertex in self.vertices:
            vertex_components = self.compute_components_of_vertex(vertex)
            for i in range(len(vertex_components)):
                components[(vertex, i)] = Component(vertex, i, vertex_components[i])
                
        return components
                
       
        
    def compute_components_of_vertex(self,vertex):
        components_vertices = self.vertices - self.closed_neighborhood(vertex)
        components = []
        visited = set()
        
        def dfs(vertex,component):
            visited.add(vertex)
            component.add(vertex)
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited and neighbor in components_vertices:
                    dfs(neighbor, component)
        
        for v in components_vertices:
            if v not in visited:
                component = set()
                dfs(v, component)
                components.append(component)
                      
        return components
    
            
    
    def closed_neighborhood(self, vertex):
        return {vertex}.union(self.adjacency_list[vertex])
    
    def closed_neighborhood_of_set(self, vertex_set):
        closed_neighborhood = set()
        for vertex in vertex_set:
            # Ensure vertex is in the correct format (e.g., string)
            vertex_str = str(vertex)
            closed_neighborhood = closed_neighborhood.union(self.closed_neighborhood(vertex_str))
        return closed_neighborhood
    
    
    
    def compute_all_intervals(self):
        intervals = {}
        for x in self.vertices:
            for y in self.vertices:
                if x != y and y not in self.adjacency_list[x]:
                    intervals[(x, y)] = Interval(x, y, self.compute_interval(x, y))
        return intervals
    
    
    def compute_interval(self, x, y):
        if y in self.adjacency_list[x]:
            raise ValueError("Vertices x and y are adjacent. Interval can only be computed for nonadjacent vertices.")

        neighbors_x = self.adjacency_list[x]
        neighbors_y = self.adjacency_list[y]

        interval = (neighbors_x.union(neighbors_y) - neighbors_x.intersection(neighbors_y)) - {x, y}
        return interval
    

    def copy(self):
        return Graph(self.num_of_vertices, self.num_of_edges, self.edges, self.vertices)

    def show(self, graph_name='graph'):
        Graph.show_count += 1
        print("Showing graph:", Graph.show_count)
        net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")

        for vertex in self.vertices:
            net.add_node(vertex)
            

        for edge in self.edges:
            u, v = edge
            net.add_edge(u, v, color="white")

        file_name = f"../output-graphs/{graph_name}-{Graph.show_count}.html"
        net.show(file_name)
