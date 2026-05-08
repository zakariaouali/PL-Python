"""
Graphical Method Solver for 2-variable Linear Programming
"""

import numpy as np
from typing import Dict, Tuple, List
import warnings

warnings.filterwarnings('ignore')


class GraphicalSolver:
    def __init__(self):
        self.objective_coeffs = None
        self.constraints = []  # List of dicts: {'A': [a, b], 'b': value, 'type': '>=', '<=', '=', 'name': 'label'}
        self.feasible_region = None
        self.vertices = []
        self.optimal_point = None
        self.optimal_value = None
        self.objective_type = 'minimize'  # 'minimize' or 'maximize'
    
    def solve(self, objective_coeffs, constraints, objective_type='minimize'):
        """
        Solve 2-variable LP graphically
        
        Parameters:
        -----------
        objective_coeffs : list [c1, c2] - coefficients of objective function
        constraints : list of dicts, each with:
            - 'A': [a, b] coefficients
            - 'b': RHS value
            - 'type': '>=', '<=', '='
            - 'name': constraint name (optional)
        objective_type : str, 'minimize' or 'maximize'
        """
        self.objective_coeffs = np.array(objective_coeffs)
        self.constraints = constraints
        self.objective_type = objective_type
        
        # Find feasible region vertices
        self.vertices = self._find_vertices()
        
        if len(self.vertices) == 0:
            return None
        
        # Evaluate objective at each vertex
        self.optimal_point, self.optimal_value = self._find_optimal_vertex()
        
        return self.optimal_point, self.optimal_value
    
    def _find_vertices(self):
        """Find all corner points of the feasible region"""
        vertices = []
        
        # Include origin if feasible
        if self._is_feasible(np.array([0, 0])):
            vertices.append(np.array([0, 0]))
        
        # Find intersections of constraint boundaries
        n_constraints = len(self.constraints)
        for i in range(n_constraints):
            for j in range(i + 1, n_constraints):
                intersection = self._find_intersection(i, j)
                if intersection is not None and self._is_feasible(intersection):
                    # Check if already in list
                    is_duplicate = False
                    for v in vertices:
                        if np.allclose(v, intersection, atol=1e-6):
                            is_duplicate = True
                            break
                    if not is_duplicate:
                        vertices.append(intersection)
        
        # Find intersections with axes (x=0 and y=0)
        # x = 0
        x_zero = self._find_x_zero_intersections()
        for point in x_zero:
            if self._is_feasible(point):
                is_duplicate = False
                for v in vertices:
                    if np.allclose(v, point, atol=1e-6):
                        is_duplicate = True
                        break
                if not is_duplicate:
                    vertices.append(point)
        
        # y = 0
        y_zero = self._find_y_zero_intersections()
        for point in y_zero:
            if self._is_feasible(point):
                is_duplicate = False
                for v in vertices:
                    if np.allclose(v, point, atol=1e-6):
                        is_duplicate = True
                        break
                if not is_duplicate:
                    vertices.append(point)
        
        return vertices
    
    def _find_intersection(self, i, j):
        """Find intersection of two constraint lines"""
        try:
            A_matrix = np.array([
                self.constraints[i]['A'],
                self.constraints[j]['A']
            ])
            b_vector = np.array([
                self.constraints[i]['b'],
                self.constraints[j]['b']
            ])
            
            intersection = np.linalg.solve(A_matrix, b_vector)
            
            # Check for non-negative constraints
            if np.any(intersection < -1e-10):
                return None
            
            return intersection
        except np.linalg.LinAlgError:
            return None
    
    def _find_x_zero_intersections(self):
        """Find points where x = 0"""
        points = []
        for constraint in self.constraints:
            a, b = constraint['A']
            if abs(b) > 1e-10:  # b coefficient is non-zero
                y = constraint['b'] / b
                if y >= -1e-10:
                    point = np.array([0, y])
                    points.append(point)
        return points
    
    def _find_y_zero_intersections(self):
        """Find points where y = 0"""
        points = []
        for constraint in self.constraints:
            a, b = constraint['A']
            if abs(a) > 1e-10:  # a coefficient is non-zero
                x = constraint['b'] / a
                if x >= -1e-10:
                    point = np.array([x, 0])
                    points.append(point)
        return points
    
    def _is_feasible(self, point):
        """Check if a point satisfies all constraints"""
        x, y = point
        
        # Non-negativity
        if x < -1e-10 or y < -1e-10:
            return False
        
        # All constraints
        for constraint in self.constraints:
            a, b = constraint['A']
            value = a * x + b * y
            c_type = constraint['type']
            c_b = constraint['b']
            
            if c_type == '>=':
                if value < c_b - 1e-10:
                    return False
            elif c_type == '<=':
                if value > c_b + 1e-10:
                    return False
            elif c_type == '=':
                if abs(value - c_b) > 1e-10:
                    return False
        
        return True
    
    def _find_optimal_vertex(self):
        """Find the optimal vertex"""
        best_point = None
        best_value = None
        
        for vertex in self.vertices:
            c1, c2 = self.objective_coeffs
            value = c1 * vertex[0] + c2 * vertex[1]
            
            if best_value is None:
                best_point = vertex
                best_value = value
            else:
                if self.objective_type == 'minimize':
                    if value < best_value:
                        best_point = vertex
                        best_value = value
                else:
                    if value > best_value:
                        best_point = vertex
                        best_value = value
        
        return best_point, best_value
    
    def get_constraint_line_points(self, constraint_idx, x_range=(0, 10)):
        """Get points for plotting constraint line"""
        constraint = self.constraints[constraint_idx]
        a, b = constraint['A']
        c = constraint['b']
        
        x_min, x_max = x_range
        
        if abs(b) > 1e-10:
            # y = (c - a*x) / b
            y_min = (c - a * x_min) / b
            y_max = (c - a * x_max) / b
            return [x_min, x_max], [y_min, y_max]
        elif abs(a) > 1e-10:
            # x = c / a (vertical line)
            x_val = c / a
            return [x_val, x_val], [x_range[0], x_range[1]]
        
        return None
    
    def get_results_table_data(self):
        """Get data for results table"""
        data = []
        for i, vertex in enumerate(self.vertices):
            c1, c2 = self.objective_coeffs
            z_value = c1 * vertex[0] + c2 * vertex[1]
            data.append({
                'point': f"({vertex[0]:.4f}, {vertex[1]:.4f})",
                'x': vertex[0],
                'y': vertex[1],
                'z': z_value,
                'is_optimal': np.allclose(vertex, self.optimal_point)
            })
        
        # Sort by Z value
        data.sort(key=lambda x: x['z'], reverse=(self.objective_type == 'maximize'))
        
        return data
