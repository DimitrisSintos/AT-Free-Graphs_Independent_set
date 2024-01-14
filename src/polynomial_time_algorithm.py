from graph import Graph
from itertools import combinations



class PolynomialTimeAlgorithm:
    def __init__(self,graph : Graph, weight : int):
        self.graph = graph
        self.weight = weight
        self.intervals = {}




    def computing_independent_set_number(self):
        # Step 1. For every x ∈ V compute all components C1x , C2x , . . . , Cr(x)
        # Step 2. For every pair of nonadjacent vertices x and y compute the interval I(x, y).
        # Step 3. Sort all the components and intervals according to nondecreasing number of
        # vertices.
        # Step 4. Compute α(C) and α(I) for each component C and each interval I in the
        # order of Step 3.
        # Step 5. Compute α(G).

        # Step 1
        self.graph.compute_all_components()
        print("\nComponents:")
        for component in self.graph.components.values():
            print(component)
            
        print("self.graph.num_of_components:", self.graph.num_of_components)
            
        
        
        # Step 2
        self.graph.compute_all_intervals()
        print("\nIntervals:")
        for interval in self.graph.intervals.values():
            print(interval)
                
        # Step 3
        sorted_components = sorted(self.graph.components.keys(), key=lambda x: len(self.graph.components[x]))
        print("\nSorted components:", sorted_components, len(sorted_components), type(sorted_components))
        
        
        sorted_intervals = sorted(self.graph.intervals.keys(), key=lambda x: len(self.graph.intervals[x]))
        print("\nSorted intervals:", sorted_intervals, len(sorted_intervals), type(sorted_intervals))
        
        # Step 4
        for key in sorted_components:
            self.alpha_C(key)
            
        # Step 5
        print('\n\n\n')
        print("Graph intependent set number:", self.alpha_G())
            
        
        
    
    def alpha_C(self,component_key):
        component = self.graph.components[component_key]
        print(component)
        if component.alpha is not None:
            return component.alpha
        
        x = component.x
        
        component_vertices = component.vertices

        max_alpha = 0
        for y in component_vertices: # y E Cx
            alpha_I_xy = self.alpha_I((x, y))
            print("alpha_I_xy:", alpha_I_xy) 
            alpha_D_sum = sum(self.alpha_C(D_iy) for D_iy in self.compute_D_iy(y, component_vertices))
            max_alpha = max(max_alpha, alpha_I_xy + alpha_D_sum)


        alpha_value = 1 + max_alpha
        
        component.alpha = alpha_value
        
    
        print('Computed Component Alpha', self.graph.components[component_key])
        return alpha_value
    
    def alpha_I(self, I):
        
        try:
            interval = self.graph.intervals[I]
            print("Interval:", interval)
            if interval.alpha is not None:
                return interval.alpha
            
            x = interval.x
            y = interval.y
            I_vertices = interval.vertices
            print("I_vertices:", I_vertices)
            
            

            max_alpha = 0
            for s in I_vertices: 
                alpha_I_xs = self.alpha_I((x, s)) 
                alpha_I_sy = self.alpha_I((s, y))
                alpha_C_sum = sum(self.alpha_C(C_is) for C_is in self.compute_C_is(s, I_vertices))
                max_alpha = max(max_alpha, alpha_I_xs + alpha_I_sy + alpha_C_sum)
                
            
            
           
            alpha_value = 1 + max_alpha
            
            interval.alpha = alpha_value
            
            
            print('Computed Interval alpha:', self.graph.intervals[I] )
            
            return alpha_value
        except:
            print("Interval", I, "not found")
            return 0

    def compute_components_subset(self, vertex, target_vertices, num_components):
        """
        Computes the components of G - N[vertex] contained in the target set.
        
        :param vertex: The vertex whose neighborhood defines the components.
        :param target_vertices: The set of vertices that the component should be a subset of.
        :param num_components: The number of components to consider.
        :return: A list of component keys whose vertices are a subset of the target set.
        """
        computed_components = []
        
        for i in range(num_components):
            component_key = (vertex, i)
            component = self.graph.components[component_key]
            if component.vertices.issubset(target_vertices):
                computed_components.append(component_key)
                    
        return computed_components

    def compute_D_iy(self, y, Cx_vertices):
        """
        D_iy are the components of G - N[y] contained in Cx.
        """
        return self.compute_components_subset(y, Cx_vertices, self.graph.num_of_components[y])

    def compute_C_is(self, s, I_vertices):
        """
        C_is are the components of G - N[s] contained in I.
        """
        return self.compute_components_subset(s, I_vertices, self.graph.num_of_components[s])
    
    def alpha_G(self):
        """
        G is the graph
        """
        
        max_alpha = 0
        max_alpha_component = None
        for x in self.graph.vertices:
            alpha_C_sum = sum(self.alpha_C((x,i)) for i in range(self.graph.num_of_components[x]))
            if max_alpha < alpha_C_sum:
                max_alpha = alpha_C_sum
                max_alpha_component = x
                    
            
        print("max_alpha_component:", max_alpha_component)
        independent_set = self.compute_independent_set(max_alpha_component)
        print("max independent set:", independent_set)
        self.graph.independent_set = independent_set
        # self.graph.show()
        return max_alpha + 1
    
    def compute_independent_set(self, x):
        independent_set = set()
        independent_set.add(x)
        print("independent_set:", independent_set)
        
        for i in range(self.graph.num_of_components[x]):
            component_key = (x, i)
            component = self.graph.components[component_key]
            vertices_added = 0
            
            for vertex in component.vertices:
                if vertex not in independent_set and self.not_adjacent_to_set(vertex, independent_set):
                    independent_set.add(vertex)
                    print("independent_set:", independent_set)
                    vertices_added += 1
                
                if vertices_added == component.alpha:
                    break
                
        return independent_set

    def not_adjacent_to_set(self, vertex, independent_set):
        for neighbor in self.graph.adjacency_list[vertex]:
            if neighbor in independent_set:
                return False
        return True

    def run(self):
        return self.computing_independent_set_number()