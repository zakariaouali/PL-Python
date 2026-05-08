"""
Chapitre 2 — Simplex Algorithm Implementation
==============================================

Implements the exact algorithm described in Chapitre 2:
  - PHASE 0: Problem Setup (check objective sense, transform constraints, build dual if MIN)
  - PHASE 1: Build Initial Tableau
  - PHASE 2: Iterate using simplex method
  - PHASE 3: Extract Solution

The solver works with both minimization and maximization problems,
automatically converting MIN problems with >= constraints to dual MAX problems with <= constraints.
"""

import numpy as np


class SimplexSolver:
    """
    Simplex Algorithm Solver following Chapitre 2 steps.
    
    Solves problems of the form:
      MIN/MAX Z = c · x
      s.c. A · x >=/<=/= b
           x >= 0
    """

    def __init__(self):
        self.tableaux = []          # List of tableau dictionaries
        self.basis_history = []     # Basis at each iteration
        self.pivot_history = []     # (row, col) pivot positions
        self.optimal_value = None   # Z* value
        self.optimal_basis = {}     # {var_name: value}
        self.n_orig = 0             # Number of original variables
        self.n_slack = 0            # Number of slack variables
        self.all_var_names = []     # All variable names (x + slack)
        self.status = ""            # "optimal", "unbounded", "infeasible"
        self._optimal_solution_array = None
        self._is_primal_min = False
        self._primal_transformation = None

    def solve(self, c, A, b, var_names=None, constraint_names=None, is_minimization=False):
        """
        Solve a linear programming problem following Chapitre 2 steps.
        
        Parameters
        ----------
        c : array-like, shape (n,)
            Objective function coefficients
        A : array-like, shape (m, n)
            Constraint matrix
        b : array-like, shape (m,)
            RHS values
        var_names : list of str, optional
            Names of original variables
        constraint_names : list of str, optional
            Names of constraints
        is_minimization : bool
            True if minimizing, False if maximizing
            
        Returns
        -------
        dict with keys: 'status', 'optimal_value', 'optimal_basis', 'tableaux', etc.
        """
        c = np.array(c, dtype=float)
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        # =====================================================================
        # PHASE 0: Problem Setup
        # =====================================================================
        
        # Step 1: Check objective sense
        self._is_primal_min = is_minimization
        
        # Store original problem for primal solution extraction
        c_primal = c.copy()
        A_primal = A.copy()
        b_primal = b.copy()
        n_primal_vars = len(c)
        n_primal_constraints = len(b)
        
        if is_minimization:
            # For MIN problem with >= constraints, convert to dual
            # MIN c·x s.t. A·x >= b  →  MAX b'y s.t. A'y <= c
            c = b_primal  # Dual objective coefficients = primal RHS
            A = A_primal.T  # Dual constraint matrix = transpose of primal matrix
            b = c_primal  # Dual RHS = primal objective coefficients
            
            # Rename variables for dual
            if var_names is None:
                var_names = [f"y{i+1}" for i in range(n_primal_constraints)]
            else:
                var_names = [f"y{i+1}" for i in range(n_primal_constraints)]
            
            # Store for primal recovery
            self._primal_transformation = {
                'type': 'primal_to_dual',
                'primal_vars': n_primal_vars,
                'primal_constraints': n_primal_constraints,
            }
            
            # For dual, the constraint names should reflect primal variables
            if var_names is None or len(var_names) < n_primal_constraints:
                constraint_names = [f"x{i+1}_limit" for i in range(n_primal_vars)]
        else:
            # MAX problem: convert >= constraints to <= for standard form
            # MAX c·x s.t. A·x >= b  →  MAX c·x s.t. -A·x <= -b
            A = -A_primal
            b = -b_primal
            self._primal_transformation = None
        
        # Step 2: Prepare standard form
        # All constraints should now be in a form suitable for simplex
        
        n_vars = len(c)
        n_constraints = len(b)
        
        self.n_orig = n_vars
        self.n_slack = n_constraints
        
        if var_names is None:
            var_names = [f"x{i+1}" for i in range(n_vars)]
        
        slack_names = [f"e{i+1}" for i in range(n_constraints)]
        if constraint_names is None:
            constraint_names = [f"C{i+1}" for i in range(n_constraints)]
        
        self.all_var_names = var_names + slack_names
        
        # =====================================================================
        # PHASE 1: Build Initial Tableau
        # =====================================================================
        
        # Build initial tableau for standard form
        # Note: We're working with >= constraints converted to <= by multiplying by -1
        # Structure: [A | I | b] with Z row = [-c | 0 | 0]
        n_cols = n_vars + n_constraints + 1  # +1 for RHS
        n_rows = n_constraints + 1           # +1 for Z row
        
        T = np.zeros((n_rows, n_cols))
        T[:n_constraints, :n_vars] = A
        T[:n_constraints, n_vars:n_vars + n_constraints] = np.eye(n_constraints)
        T[:n_constraints, -1] = b
        T[n_constraints, :n_vars] = -c
        
        basis = list(range(n_vars, n_vars + n_constraints))
        
        self._save_tableau(T, basis, iteration=0,
                          entering=None, leaving=None,
                          pivot_rc=None,
                          var_names=self.all_var_names,
                          constraint_names=constraint_names)
        
        # Step 6: Check initial feasibility
        if np.any(T[:n_constraints, -1] < -1e-9):
            self.status = "infeasible"
            self.optimal_value = 0.0  # Set to 0 for infeasible problems
            self.optimal_basis = {}   # No solution for infeasible problems
            return self._get_result()
        
        # =====================================================================
        # PHASE 2: Iterate
        # =====================================================================
        
        iteration = 0
        MAX_ITER = 100
        
        while iteration < MAX_ITER:
            # Step 7: Optimality check (check Z row)
            z_row = T[n_constraints, :-1]
            min_coeff = np.min(z_row)
            
            if min_coeff >= -1e-9:  # All coefficients >= 0
                self.status = "optimal"
                break
            
            # Step 8: Choose entering variable (most negative coefficient in Z row)
            entering_col = int(np.argmin(z_row))
            
            # Step 9: Choose leaving variable (minimum ratio test)
            col_vals = T[:n_constraints, entering_col]
            rhs_vals = T[:n_constraints, -1]
            
            ratios = np.full(n_constraints, np.inf)
            for i in range(n_constraints):
                if col_vals[i] > 1e-9:
                    ratios[i] = rhs_vals[i] / col_vals[i]
            
            if np.all(ratios == np.inf):
                self.status = "unbounded"
                self.optimal_value = float('inf')  # Unbounded solution
                break
            
            leaving_row = int(np.argmin(ratios))
            
            # Step 10: Pivot operation
            T = self._pivot(T, leaving_row, entering_col)
            
            # Update basis
            old_basis_var = basis[leaving_row]
            basis[leaving_row] = entering_col
            
            iteration += 1
            self.pivot_history.append((leaving_row, entering_col))
            
            self._save_tableau(T, basis, iteration=iteration,
                              entering=entering_col,
                              leaving=old_basis_var,
                              pivot_rc=(leaving_row, entering_col),
                              var_names=self.all_var_names,
                              constraint_names=constraint_names)
        
        if iteration >= MAX_ITER:
            self.status = "max_iterations_reached"
        
        # =====================================================================
        # PHASE 3: Extract Solution
        # =====================================================================
        
        # Step 12: Read optimal value
        self.optimal_value = T[n_constraints, -1]
        
        # Step 13: Read basic variable values
        self.optimal_basis = {}
        for row_idx, var_idx in enumerate(basis):
            self.optimal_basis[self.all_var_names[var_idx]] = T[row_idx, -1]
        
        # For dual problem, recover primal solution from reduced costs
        if self._primal_transformation and self._primal_transformation['type'] == 'primal_to_dual':
            # Primal solution x[i] = reduced cost of slack variable e[i] in dual
            # Reduced cost = coefficient in Z row
            self._recover_primal_solution(T, n_primal_vars, n_primal_constraints)
        
        # Mark final tableau as optimal
        if len(self.tableaux) > 0:
            self.tableaux[-1]["is_optimal"] = True
        
        self.basis_history = [t["basis_names"] for t in self.tableaux]
        
        return self._get_result()

    def _recover_primal_solution(self, T, n_primal_vars, n_primal_constraints):
        """
        For dual problem, extract primal solution from reduced costs of dual slacks.
        
        In the dual tableau:
        - Columns 0:n_primal_constraints are dual variables y
        - Columns n_primal_constraints:n_primal_constraints+n_primal_vars are slack variables
        
        The reduced cost of slack[i] in the Z row gives the primal variable x[i]
        """
        # The Z row values for slack columns directly give the reduced costs of primal variables
        if len(self.tableaux) > 0:
            final_tab = self.tableaux[-1]['tableau']
            z_row_idx = final_tab.shape[0] - 1
            z_row = final_tab[z_row_idx, :]
            
            # Initialize primal solution array
            primal_sol = np.zeros(n_primal_vars)
            
            # Slack variables start after dual variables
            slack_start_col = n_primal_constraints
            
            # For each primal variable i, its value is the Z row coefficient for slack e[i]
            # (these are reduced costs, which equal the primal variable values by complementary slackness)
            for i in range(n_primal_vars):
                slack_col = slack_start_col + i
                if slack_col < len(z_row):
                    # The Z row value IS the reduced cost for non-basic variables
                    # or 0 for basic variables (but slacks won't be basic in optimal solution)
                    primal_sol[i] = max(0, z_row[slack_col])
            
            self._optimal_solution_array = primal_sol

    def _pivot(self, T, pivot_row, pivot_col):
        """Perform pivot operation (Gaussian elimination)"""
        T = T.copy()
        pivot_element = T[pivot_row, pivot_col]
        
        # Normalize pivot row
        T[pivot_row, :] /= pivot_element
        
        # Eliminate pivot column in other rows
        for i in range(len(T)):
            if i != pivot_row:
                factor = T[i, pivot_col]
                T[i, :] -= factor * T[pivot_row, :]
        
        return T

    def _save_tableau(self, T, basis, iteration, entering, leaving, pivot_rc,
                     var_names, constraint_names):
        """Save tableau snapshot for display"""
        n_constraints = len(T) - 1
        basis_names = [var_names[b] for b in basis]
        
        # Non-basis variables
        all_indices = set(range(len(var_names)))
        basis_set = set(basis)
        nonbasis_idx = sorted(all_indices - basis_set)
        nonbasis_names = [var_names[i] for i in nonbasis_idx]
        
        # Basis values
        basis_values = {basis_names[i]: T[i, -1] for i in range(n_constraints)}
        
        # Variable names
        entering_name = var_names[entering] if entering is not None else None
        leaving_name = var_names[leaving] if leaving is not None else None
        
        # Tableau data
        tableau_data = np.round(T.copy(), 6)
        
        self.tableaux.append({
            'iteration': iteration,
            'tableau': tableau_data,
            'basis': basis.copy(),
            'basis_names': basis_names,
            'nonbasis_names': nonbasis_names,
            'basis_values': basis_values,
            'entering': entering_name,
            'leaving': leaving_name,
            'pivot_rc': pivot_rc,
            'var_names': var_names,
            'constraint_names': constraint_names,
            'is_optimal': False,
        })

    def _get_result(self):
        """Return result dictionary"""
        return {
            'status': self.status,
            'optimal_value': self.optimal_value,
            'optimal_basis': self.optimal_basis,
            'tableaux': self.tableaux,
            'basis_history': self.basis_history,
            'pivot_history': self.pivot_history,
            'all_var_names': self.all_var_names,
        }

    @property
    def optimal_solution(self):
        """Get optimal solution as array (original variables only)"""
        if self._optimal_solution_array is None:
            # For primal-to-dual: _recover_primal_solution should have set this
            # For direct solve: extract from optimal_basis
            var_names = self.all_var_names[:self.n_orig]
            sol = np.array([self.optimal_basis.get(v, 0.0) for v in var_names])
            self._optimal_solution_array = sol
        return self._optimal_solution_array

    def get_tableau_arrays(self):
        """Get tableau arrays for display"""
        return [t['tableau'] for t in self.tableaux]

    def set_constraint_transformations(self, transformations):
        """Store constraint transformations for display"""
        self._constraint_transformations = transformations


# ============================================================================
# Test function
# ============================================================================

def get_default_problem():
    """Get a default test problem"""
    # MIN: 250x + 200y + 150z
    # s.t. 30x + 5y + 10z >= 60 (Proteins)
    #      10x + 2y + 5z <= 50 (Lipids) - will be converted to >= by GUI
    #      40y + 20z >= 100 (Carbs)
    #      5x + 3y + 8z >= 30 (Fiber)
    
    c = [250, 200, 150]
    A = [
        [30, 5, 10],
        [10, 2, 5],
        [0, 40, 20],
        [5, 3, 8],
    ]
    b = [60, 50, 100, 30]
    var_names = ["Chicken", "Rice", "Vegetables"]
    constraint_names = ["Proteins", "Lipids", "Carbs", "Fiber"]
    
    return c, A, b, var_names, constraint_names


if __name__ == "__main__":
    c, A, b, var_names, constraint_names = get_default_problem()
    
    solver = SimplexSolver()
    result = solver.solve(c, A, b, var_names, constraint_names, is_minimization=True)
    
    print(f"\nStatus: {result['status']}")
    print(f"Optimal Value: {result['optimal_value']:.4f}")
    print("\nOptimal Solution:")
    for var, val in result['optimal_basis'].items():
        if not var.startswith('e'):  # Show only original variables
            print(f"  {var} = {val:.4f}")
    
    print(f"\nIterations: {len(result['tableaux']) - 1}")
