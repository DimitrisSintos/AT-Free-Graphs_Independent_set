from graph import Graph
from itertools import combinations



class PolynomialTimeAlgorithm:
    def __init__(self,graph : Graph, weight : int):
        self.graph = graph
        self.weight = weight
        self.components = {}
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
        self.components = self.graph.compute_all_components()
        print("\nComponents:")
        for component in self.components.values():
            print(component)
        
        # Step 2
        self.intervals = self.graph.compute_all_intervals()
        print("\nIntervals:")
        for interval in self.intervals.values():
            print(interval)
                
        # Step 3
        sorted_components = sorted(self.components.keys(), key=lambda x: len(self.components[x]))
        print("\nSorted components:", sorted_components, len(sorted_components), type(sorted_components))
        
        
        sorted_intervals = sorted(self.intervals.keys(), key=lambda x: len(self.intervals[x]))
        print("\nSorted intervals:", sorted_intervals, len(sorted_intervals), type(sorted_intervals))
        
        # Step 4
        for key in sorted_intervals:
            self.alpha_I(key)
            
        for key in sorted_components:
            self.alpha_C(key)
            
        # Step 5
        print('\n\n\n')
        print("Graph intependent set number:", self.alpha_G())
            
        
        
    
    def alpha_C(self,component_key):
        component = self.components[component_key]
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

        if component.alpha is not None:
            return component.alpha
        alpha_value = 1 + max_alpha
        
        component.alpha = alpha_value
        self.components[component_key] = component
        
    
        print('Computed Component Alpha', self.components[component_key])
        return alpha_value
    
    def alpha_I(self, I):
        
        try:
        
            interval = self.intervals[I]
            print("Interval:", interval)
            if interval.alpha is not None:
                return interval.alpha
            
            x = interval.x
            y = interval.y
            I_vertices = interval.vertices
            print("I_vertices:", I_vertices)
            
            

            max_alpha = 0
            for s in I_vertices:  # Assuming I is an iterable of vertices
                alpha_I_xs = self.alpha_I((x, s))  # Assuming x and y are known in the context
                alpha_I_sy = self.alpha_I((s, y))
                alpha_C_sum = sum(self.alpha_C(C_is) for C_is in self.compute_C_is(s, I_vertices))
                max_alpha = max(max_alpha, alpha_I_xs + alpha_I_sy + alpha_C_sum)
                
            
            
            if interval.alpha is not None:
                return interval.alpha
            alpha_value = 1 + max_alpha
            
            interval.alpha = alpha_value
            self.intervals[I] = interval
            
            
            print('Computed Interval alpha:', self.intervals[I] )
            
            return alpha_value
        except:
            return 0

    def compute_D_iy(self, y, Cx_vertices):
        """
        D_iy are the components og G - N[y] contained in Cx
        
        """
        
        computed_D_iy = []
        
        for component_key in self.components:
            if component_key[0]== y:
                component = self.components[component_key]
                if component.vertices.issubset(Cx_vertices):
                    computed_D_iy.append(component_key)
                    
        return computed_D_iy
    
    def compute_C_is(self, s, I_vertices):
        """
        C_is are the components of G - N[s] contained in I
        
        """
        
        computed_C_is = []
        
        for component_key in self.components:
            if component_key[0]== s:
                component = self.components[component_key]
                if component.vertices.issubset(I_vertices):
                    computed_C_is.append(component_key)
                    
        return computed_C_is
    
    def alpha_G(self):
        """
        G is the graph
        """
        
        max_alpha = 0
        for x in self.graph.vertices:
            x_components = []
            for component_key in self.components:
                if component_key[0]== x:
                    x_components.append(component_key)
                    
            alpha_C_sum = sum(self.alpha_C(component_key) for component_key in x_components)
            max_alpha = max(max_alpha, alpha_C_sum)
            
        return max_alpha

    def run(self):
        return self.computing_independent_set_number()