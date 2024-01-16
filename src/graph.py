from itertools import combinations
from pyvis.network import Network
from component import Component
from interval import Interval

import os


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
            
        self.components = {}
        self.num_of_components = {}
        self.intervals = {}
        
        self.independent_set = set()
            
    
    def compute_all_components(self):
        for vertex in self.vertices:
            vertex_components = self.compute_components_of_vertex(vertex)
            self.num_of_components[vertex] = len(vertex_components)
            for i in range(len(vertex_components)):
                self.components[(vertex, i)] = Component(vertex, i, vertex_components[i])
                
        
                
       
        
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
        for x in self.vertices:
            for y in self.vertices:
                if x != y and y not in self.adjacency_list[x]:
                    interval = self.compute_interval(x, y)
                    if interval:
                        self.intervals[(x, y)] = Interval(x, y, interval)
        return self.intervals
    
    
    def compute_interval(self, x, y):
        if y in self.adjacency_list[x]:
            raise ValueError("Vertices x and y are adjacent. Interval can only be computed for nonadjacent vertices.")

        Cx_y = None
        Cy_x = None
        
        #TODO: For all nonadjacent vertices x and x there is a pointer P(x,y) to the list of Cx_y
        for i in range(self.num_of_components[x]):
            component = self.components[(x, i)]
            if y in component.vertices:
                Cx_y = component.vertices
                break
        
        for i in range(self.num_of_components[y]):
            component = self.components[(y, i)]
            if x in component.vertices:
                Cy_x = component.vertices
                break
            
        # print("Cx_y:", Cx_y)
        # print("Cy_x:", Cy_x)

        interval = Cx_y.intersection(Cy_x) if Cx_y is not None and Cy_x is not None else None
        return interval
    

    def copy(self):
        return Graph(self.num_of_vertices, self.num_of_edges, self.edges, self.vertices)

    def show(self, graph_name='graph'):
        Graph.show_count += 1
        print("Showing graph:", Graph.show_count)
        net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")

        for vertex in self.vertices:
            if vertex in self.independent_set:
                net.add_node(vertex, color="red")
            else:
                net.add_node(vertex)
            

        for edge in self.edges:
            u, v = edge
            net.add_edge(u, v, color="white")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(script_dir, '..', 'output-graphs')
        file_name = os.path.join(output_dir, f"{graph_name}-{Graph.show_count}.html")
        net.show(file_name)
