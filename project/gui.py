"""
Tkinter GUI for Personalized Food Optimization System
PROFESSIONAL REDESIGN - Modern UX/UI with responsive layout
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import os

from graphical_solver import GraphicalSolver
from simplex_solver import SimplexSolver


# Professional Color Palette
COLORS = {
    'bg_primary': "#0a0e27",
    'bg_secondary': "#141829",
    'bg_tertiary': "#1d2439",
    'accent_cyan': "#00d9ff",
    'accent_green': "#00ff88",
    'accent_gold': "#ffd700",
    'text_primary': "#ffffff",
    'text_secondary': "#b0b8cc",
    'text_muted': "#6b7280",
    'border': "#2d3748"
}


class FoodOptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Système d'Optimisation Alimentaire Personnalisée")
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)
        self.root.resizable(True, True)
        self.root.configure(bg=COLORS['bg_primary'])
        
        self._setup_theme()
        self._create_ui()
    
    def _create_ui(self):
        """Create main UI"""
        main_frame = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_frame.pack(fill="both", expand=True)
        
        # Header
        self._create_header(main_frame)
        
        # Tabs
        notebook_frame = tk.Frame(main_frame, bg=COLORS['bg_primary'])
        notebook_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill="both", expand=True)
        
        # Home tab
        self.home_frame = HomeTab(self.notebook)
        self.notebook.add(self.home_frame, text="🏠 HOME")
        
        # Chapter 1 tab
        self.chapter1_frame = Chapter1Tab(self.notebook)
        self.notebook.add(self.chapter1_frame, text="📈 Graphical Method")
        
        # Chapter 2 tab
        self.chapter2_frame = Chapter2Tab(self.notebook)
        self.notebook.add(self.chapter2_frame, text="🔢 Simplex Algorithm")
    
    def _create_header(self, parent):
        """Create professional header"""
        header = tk.Frame(parent, bg=COLORS['bg_secondary'], height=80)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg=COLORS['bg_secondary'])
        title_frame.pack(side="left", fill="both", expand=True, padx=30, pady=15)
        
        # Main title with gradient effect
        title = tk.Label(title_frame, text="🍽️  Personalized Food Optimization System",
                        font=("Segoe UI", 18, "bold"), fg=COLORS['accent_cyan'],
                        bg=COLORS['bg_secondary'], anchor="w")
        title.pack(anchor="w", pady=(5, 8))
        
        # Subtitle with status
        subtitle = tk.Label(title_frame, text="Linear Programming Solver • Graphical & Simplex Methods",
                           font=("Segoe UI", 10), fg=COLORS['accent_green'],
                           bg=COLORS['bg_secondary'], anchor="w")
        subtitle.pack(anchor="w")
        
        # Version/status info on right
        info_frame = tk.Frame(header, bg=COLORS['bg_secondary'])
        info_frame.pack(side="right", fill="y", padx=30)
        
        version = tk.Label(info_frame, text="v1.0.0 • Ready",
                          font=("Segoe UI", 9), fg=COLORS['accent_gold'],
                          bg=COLORS['bg_secondary'])
        version.pack(pady=5)
        
        # Divider with accent color
        divider = tk.Frame(parent, bg=COLORS['accent_cyan'], height=3)
        divider.pack(fill="x", padx=0, pady=0)
    
    def _setup_theme(self):
        """Configure professional theme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure notebook tabs with modern styling
        style.configure('TNotebook', background=COLORS['bg_primary'], borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 14], font=('Segoe UI', 10, 'bold'),
                       background=COLORS['bg_tertiary'], foreground=COLORS['text_secondary'])
        style.map('TNotebook.Tab', 
                 background=[('selected', COLORS['accent_cyan']),
                            ('active', COLORS['bg_secondary'])],
                 foreground=[('selected', COLORS['bg_primary']),
                            ('active', COLORS['accent_cyan'])])
        
        # Configure frames with modern flat design
        style.configure('TFrame', background=COLORS['bg_primary'])
        style.configure('TLabel', background=COLORS['bg_primary'], foreground=COLORS['text_primary'],
                       font=('Segoe UI', 10))
        
        # Configure buttons with modern styling
        style.configure('TButton', background=COLORS['accent_cyan'], foreground=COLORS['bg_primary'],
                       font=('Segoe UI', 10, 'bold'), borderwidth=0, relief='flat', padding=10)
        style.map('TButton', 
                 background=[('active', COLORS['accent_green']),
                            ('pressed', COLORS['accent_gold']),
                            ('disabled', COLORS['text_muted'])],
                 foreground=[('disabled', COLORS['bg_tertiary'])])
        
        # Configure input fields
        style.configure('TEntry', fieldbackground=COLORS['bg_tertiary'],
                       foreground=COLORS['text_primary'], font=('Segoe UI', 10),
                       borderwidth=1, relief='solid')
        style.configure('TCombobox', fieldbackground=COLORS['bg_tertiary'],
                       foreground=COLORS['text_primary'], font=('Segoe UI', 10),
                       borderwidth=1, relief='solid')
        
        # Configure treeview with enhanced styling
        style.configure('Treeview', background=COLORS['bg_tertiary'], foreground=COLORS['text_primary'],
                       fieldbackground=COLORS['bg_tertiary'], font=('Segoe UI', 9), rowheight=24, 
                       borderwidth=1, relief='solid')
        style.configure('Treeview.Heading', background=COLORS['bg_secondary'],
                       foreground=COLORS['accent_cyan'], font=('Segoe UI', 10, 'bold'), 
                       borderwidth=1, relief='raised')
        style.map('Treeview', 
                 background=[('selected', COLORS['accent_cyan']),
                            ('alternate', COLORS['bg_secondary'])],
                 foreground=[('selected', COLORS['bg_primary'])])
        
        # Configure scrollbars
        style.configure('Vertical.TScrollbar', background=COLORS['bg_tertiary'],
                       darkcolor=COLORS['border'], lightcolor=COLORS['bg_secondary'],
                       borderwidth=0, arrowcolor=COLORS['accent_cyan'])
        style.configure('Horizontal.TScrollbar', background=COLORS['bg_tertiary'],
                       darkcolor=COLORS['border'], lightcolor=COLORS['bg_secondary'],
                       borderwidth=0, arrowcolor=COLORS['accent_cyan'])


class HomeTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(style='TFrame')
        
        # Main container
        main = tk.Frame(self, bg=COLORS['bg_primary'])
        main.pack(fill="both", expand=True)
        
        # Hero Section
        self._create_hero(main)
        
        # Main Content
        content_frame = tk.Frame(main, bg=COLORS['bg_primary'])
        content_frame.pack(fill="both", expand=True, padx=50, pady=40)
        
        # Quick Info Section
        self._create_quick_info(content_frame)
        
        # Footer
        self._create_simple_footer(main)
    
    def _create_hero(self, parent):
        """Minimalist hero section"""
        hero = tk.Frame(parent, bg=COLORS['bg_secondary'], height=200)
        hero.pack(fill="x", padx=0, pady=0)
        hero.pack_propagate(False)
        
        # Center content vertically and horizontally
        wrapper = tk.Frame(hero, bg=COLORS['bg_secondary'])
        wrapper.pack(fill="both", expand=True)
        
        # Main title only
        title = tk.Label(wrapper, text="Personalized Food Optimization",
                        font=("Segoe UI", 28, "bold"), fg=COLORS['accent_cyan'],
                        bg=COLORS['bg_secondary'])
        title.pack(anchor="center", pady=(30, 10))
        
        # Short description
        desc = tk.Label(wrapper, text="Linear Programming Solver for Optimal Nutrition",
                       font=("Segoe UI", 10), fg=COLORS['text_secondary'],
                       bg=COLORS['bg_secondary'])
        desc.pack(anchor="center", pady=(0, 30))
    
    def _create_quick_info(self, parent):
        """Simple info cards"""
        # Title
        title = tk.Label(parent, text="Overview", font=("Segoe UI", 14, "bold"),
                        fg=COLORS['accent_cyan'], bg=COLORS['bg_primary'])
        title.pack(anchor="w", pady=(0, 20))
        
        # Cards container
        cards_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        cards_frame.pack(fill="x")
        
        # Left column
        left = tk.Frame(cards_frame, bg=COLORS['bg_primary'])
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        # Right column
        right = tk.Frame(cards_frame, bg=COLORS['bg_primary'])
        right.pack(side="left", fill="both", expand=True, padx=(15, 0))
        
        # Project Info
        self._simple_card(left, "📌 Project",
                         ["• 2 Optimization Methods",
                          "• Support 3+ Variables",
                          "• Nutrition Focus",
                          "• Real-time Visualization"])
        
        # Features
        self._simple_card(left, "✨ Features",
                         ["• Graphical Method (2D)",
                          "• Simplex Algorithm ",
                          "• Step-by-step Iterations",
                          "• Export Results"])
        
        # Team
        self._simple_card(right, "👥 Team",
                         ["Zakaria Ait Ahmad Ouali",
                          "Mohammed Amine Mourrane",
                          "Mohammed Taha Aboundir",
                          "Aya Benohoud"])
        
        # Tech Stack
        self._simple_card(right, "🛠️ Tech Stack",
                         ["Python ",
                          "Tkinter GUI",
                          "NumPy / SciPy",
                          "Matplotlib Charts"])
    
    def _simple_card(self, parent, title, items):
        """Create a clean simple card"""
        card = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                       highlightbackground=COLORS['border'])
        card.pack(fill="x", pady=(0, 15))
        
        # Title
        title_label = tk.Label(card, text=title, font=("Segoe UI", 10, "bold"),
                              fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w")
        title_label.pack(fill="x", padx=12, pady=(10, 8))
        
        # Items
        for item in items:
            item_label = tk.Label(card, text=item, font=("Segoe UI", 9),
                                 fg=COLORS['text_secondary'], bg=COLORS['bg_tertiary'], anchor="w")
            item_label.pack(fill="x", padx=12, pady=3)
        
        # Bottom padding
        tk.Frame(card, bg=COLORS['bg_tertiary'], height=6).pack(fill="x")
    
    def _create_simple_footer(self, parent):
        """Minimal footer"""
        footer = tk.Frame(parent, bg=COLORS['bg_secondary'])
        footer.pack(fill="x", side="bottom", padx=0, pady=0)
        
        text = tk.Label(footer, text="Navigate to CHAPTER 1 (Graphical Method) or CHAPTER 2 (Simplex) to get started",
                       font=("Segoe UI", 8), fg=COLORS['text_secondary'], bg=COLORS['bg_secondary'])
        text.pack(pady=12)


class Chapter1Tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.solver = GraphicalSolver()
        self.current_solution = None
        
        # PanedWindow for responsive layout
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Left panel with scrolling
        left_cont = tk.Frame(paned, bg=COLORS['bg_primary'])
        paned.add(left_cont, weight=0)
        
        left_canvas = tk.Canvas(left_cont, bg=COLORS['bg_primary'], highlightthickness=0,
                               borderwidth=0, width=380)
        left_scroll = ttk.Scrollbar(left_cont, orient="vertical", command=left_canvas.yview)
        left_panel = ttk.Frame(left_canvas)
        
        left_panel.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        left_canvas.create_window((0, 0), window=left_panel, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scroll.set)
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scroll.pack(side="right", fill="y")
        
        # Header
        header = tk.Frame(left_panel, bg=COLORS['bg_secondary'], highlightthickness=1,
                         highlightbackground=COLORS['border'])
        header.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(header, text="GRAPHICAL METHOD", font=("Segoe UI", 13, "bold"),
                fg=COLORS['accent_cyan'], bg=COLORS['bg_secondary']).pack(pady=8)
        tk.Label(header, text="2-Variable Linear Programming", font=("Segoe UI", 9),
                fg=COLORS['text_secondary'], bg=COLORS['bg_secondary']).pack(pady=(0, 8))
        
        # Sections
        self._create_food_inputs(left_panel)
        self._create_constraints(left_panel)
        self._create_buttons(left_panel)
        self._create_results(left_panel)
        
        # Right panel
        self.right = tk.Frame(paned, bg=COLORS['bg_primary'])
        paned.add(self.right, weight=1)
        
        self._load_default()
    
    def _create_food_inputs(self, parent):
        """Food inputs section"""
        frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                        highlightbackground=COLORS['border'])
        frame.pack(fill="x", padx=10, pady=(5, 10))
        
        tk.Label(frame, text="🍗 FOODS", font=("Segoe UI", 10, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=10, pady=8)
        
        # Food 1
        f1 = tk.Frame(frame, bg=COLORS['bg_tertiary'])
        f1.pack(fill="x", padx=10, pady=(0, 8))
        tk.Label(f1, text="Food 1:", font=("Segoe UI", 9, "bold"),
                fg=COLORS['text_primary'], bg=COLORS['bg_tertiary'], width=8).pack(side="left")
        self.food1_name = ttk.Entry(f1, width=16)
        self.food1_name.pack(side="left", padx=5, fill="x", expand=True)
        self.food1_name.insert(0, "Chicken")
        tk.Label(f1, text="kcal:", font=("Segoe UI", 9), fg=COLORS['text_secondary'],
                bg=COLORS['bg_tertiary']).pack(side="left", padx=(10, 2))
        self.food1_cal = ttk.Entry(f1, width=10)
        self.food1_cal.pack(side="left", padx=2)
        self.food1_cal.insert(0, "250")
        
        # Food 2
        f2 = tk.Frame(frame, bg=COLORS['bg_tertiary'])
        f2.pack(fill="x", padx=10, pady=(0, 8))
        tk.Label(f2, text="Food 2:", font=("Segoe UI", 9, "bold"),
                fg=COLORS['text_primary'], bg=COLORS['bg_tertiary'], width=8).pack(side="left")
        self.food2_name = ttk.Entry(f2, width=16)
        self.food2_name.pack(side="left", padx=5, fill="x", expand=True)
        self.food2_name.insert(0, "Rice")
        tk.Label(f2, text="kcal:", font=("Segoe UI", 9), fg=COLORS['text_secondary'],
                bg=COLORS['bg_tertiary']).pack(side="left", padx=(10, 2))
        self.food2_cal = ttk.Entry(f2, width=10)
        self.food2_cal.pack(side="left", padx=2)
        self.food2_cal.insert(0, "200")
    
    def _create_constraints(self, parent):
        """Constraints section"""
        frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                        highlightbackground=COLORS['border'])
        frame.pack(fill="x", padx=10, pady=(5, 10))
        
        tk.Label(frame, text="📋 CONSTRAINTS", font=("Segoe UI", 10, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=10, pady=8)
        
        # Constraint rows
        defaults = [
            ('30', '5', '>=', '60'),
            ('10', '2', '<=', '50'),
            ('0', '40', '>=', '100')
        ]
        
        self.const_entries = []
        for i, (a, b, typ, val) in enumerate(defaults):
            row = tk.Frame(frame, bg=COLORS['bg_tertiary'])
            row.pack(fill="x", padx=10, pady=(0, 6))
            
            ca = ttk.Entry(row, width=6)
            ca.pack(side="left", padx=2)
            ca.insert(0, a)
            
            tk.Label(row, text="x +", font=("Segoe UI", 9), fg=COLORS['text_secondary'],
                    bg=COLORS['bg_tertiary']).pack(side="left", padx=2)
            
            cb = ttk.Entry(row, width=6)
            cb.pack(side="left", padx=2)
            cb.insert(0, b)
            
            tk.Label(row, text="y", font=("Segoe UI", 9), fg=COLORS['text_secondary'],
                    bg=COLORS['bg_tertiary']).pack(side="left", padx=2)
            
            ctype = ttk.Combobox(row, values=[">=", "<=", "="], width=4, state='readonly')
            ctype.pack(side="left", padx=2)
            ctype.set(typ)
            
            crhs = ttk.Entry(row, width=6)
            crhs.pack(side="left", padx=2)
            crhs.insert(0, val)
            
            self.const_entries.append({'a': ca, 'b': cb, 'type': ctype, 'rhs': crhs})
    
    def _create_buttons(self, parent):
        """Action buttons"""
        frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(frame, text="🔍 SOLVE", font=("Segoe UI", 10, "bold"),
                 bg=COLORS['accent_cyan'], fg=COLORS['bg_primary'],
                 activebackground=COLORS['accent_green'], command=self._solve,
                 padx=12, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=3,
                                                                        fill="both", expand=True)
        
        tk.Button(frame, text="💾 EXPORT", font=("Segoe UI", 10, "bold"),
                 bg=COLORS['accent_gold'], fg=COLORS['bg_primary'],
                 activebackground=COLORS['accent_green'], command=self._export,
                 padx=12, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=3,
                                                                        fill="both", expand=True)
        
        tk.Button(frame, text="🔄 RESET", font=("Segoe UI", 10, "bold"),
                 bg=COLORS['text_muted'], fg=COLORS['bg_primary'],
                 activebackground=COLORS['accent_green'], command=self._load_default,
                 padx=12, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=3,
                                                                        fill="both", expand=True)
    
    def _create_results(self, parent):
        """Results display"""
        frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                        highlightbackground=COLORS['border'])
        frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        tk.Label(frame, text="✨ SOLUTION", font=("Segoe UI", 10, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=10, pady=8)
        
        # Tree
        tree_f = tk.Frame(frame, bg=COLORS['bg_tertiary'])
        tree_f.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.results_tree = ttk.Treeview(tree_f, columns=('Point', 'Value'), height=6, show='headings')
        self.results_tree.column("Point", anchor=tk.CENTER, width=120)
        self.results_tree.column("Value", anchor=tk.CENTER, width=80)
        self.results_tree.heading("Point", text="Vertex (x, y)")
        self.results_tree.heading("Value", text="Z Value")
        
        scroll = ttk.Scrollbar(tree_f, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scroll.set)
        self.results_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.results_tree.tag_configure('opt', foreground=COLORS['accent_gold'],
                                       background=COLORS['bg_secondary'])
        
        # Summary
        self.sol_text = tk.Text(frame, height=5, width=40, bg=COLORS['bg_secondary'],
                               fg=COLORS['accent_cyan'], font=('Courier New', 9, 'bold'),
                               relief="flat", borderwidth=0)
        self.sol_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.sol_text.configure(state='disabled')
    
    def _load_default(self):
        self._solve()
    
    def _solve(self):
        try:
            c = [float(self.food1_cal.get()), float(self.food2_cal.get())]
            constraints = [{
                'A': [float(e['a'].get()), float(e['b'].get())],
                'b': float(e['rhs'].get()),
                'type': e['type'].get()
            } for e in self.const_entries]
            
            self.solver.solve(c, constraints, 'minimize')
            self.current_solution = {
                'c': c,
                'food1': self.food1_name.get(),
                'food2': self.food2_name.get(),
                'constraints': constraints
            }
            
            self._update_results()
            self._draw_graph()
        except Exception as e:
            messagebox.showerror("Error", f"Error solving:\n{str(e)}")
    
    def _update_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        data = self.solver.get_results_table_data()
        for item in data:
            val = (f"({item['x']:.3f}, {item['y']:.3f})", f"{item['z']:.2f}")
            tag = 'opt' if item['is_optimal'] else ''
            self.results_tree.insert('', 'end', values=val, tags=(tag,))
        
        x, y = self.solver.optimal_point
        z = self.solver.optimal_value
        
        txt = f"✓ OPTIMAL SOLUTION\n\n{self.current_solution['food1']}: {x:.4f}\n"
        txt += f"{self.current_solution['food2']}: {y:.4f}\nZ: {z:.2f} kcal"
        
        self.sol_text.configure(state='normal')
        self.sol_text.delete('1.0', tk.END)
        self.sol_text.insert('1.0', txt)
        self.sol_text.configure(state='disabled')
    
    def _draw_graph(self):
        for w in self.right.winfo_children():
            w.destroy()
        
        fig, ax = plt.subplots(figsize=(10, 7.5), facecolor=COLORS['bg_primary'])
        ax.set_facecolor(COLORS['bg_secondary'])
        
        x_range = (0, 8)
        x = np.linspace(*x_range, 300)
        colors_p = ['#ff6b6b', '#4ecdc4', '#ffe66d']
        
        for i, c in enumerate(self.current_solution['constraints']):
            a, b = c['A']
            if abs(b) > 1e-10:
                y = (c['b'] - a * x) / b
                ax.plot(x, y, color=colors_p[i], linewidth=2.5, label=f"{a:.1f}x+{b:.1f}y {c['type']} {c['b']:.1f}", alpha=0.9)
                if c['type'] == '>=':
                    ax.fill_between(x, y, 10, alpha=0.08, color=colors_p[i])
                elif c['type'] == '<=':
                    ax.fill_between(x, 0, y, alpha=0.08, color=colors_p[i])
        
        for v in self.solver.vertices:
            ax.plot(v[0], v[1], 'o', color=COLORS['accent_green'], markersize=10, zorder=5)
            ax.annotate(f'({v[0]:.2f}, {v[1]:.2f})', xy=v, xytext=(8, 8),
                       textcoords='offset points', color=COLORS['accent_green'], fontsize=8,
                       weight='bold', bbox=dict(boxstyle='round,pad=0.3',
                       facecolor=COLORS['bg_secondary'], edgecolor=COLORS['accent_green'],
                       linewidth=1, alpha=0.8))
        
        if self.solver.optimal_point is not None:
            ox, oy = self.solver.optimal_point
            ax.plot(ox, oy, marker='*', color=COLORS['accent_gold'], markersize=30,
                   label=f'Optimal: ({ox:.2f}, {oy:.2f})', zorder=6, markeredgecolor='white', markeredgewidth=1)
            ax.annotate(f'OPTIMAL\nZ={self.solver.optimal_value:.2f}', xy=(ox, oy),
                       xytext=(12, 12), textcoords='offset points',
                       color=COLORS['accent_gold'], fontsize=10, weight='bold',
                       bbox=dict(boxstyle='round', facecolor=COLORS['bg_secondary'],
                       edgecolor=COLORS['accent_gold'], linewidth=2, alpha=0.95),
                       arrowprops=dict(arrowstyle='->', color=COLORS['accent_gold'], lw=2))
        
        ax.set_xlim(x_range)
        ax.set_ylim(0, 10)
        ax.set_xlabel(f'Portion of {self.current_solution["food1"]}',
                     color=COLORS['text_primary'], fontsize=12, weight='bold')
        ax.set_ylabel(f'Portion of {self.current_solution["food2"]}',
                     color=COLORS['text_primary'], fontsize=12, weight='bold')
        ax.set_title('Feasible Region & Optimal Solution',
                    color=COLORS['accent_cyan'], fontsize=13, weight='bold', pad=20)
        ax.legend(loc='upper right', facecolor=COLORS['bg_secondary'],
                 edgecolor=COLORS['accent_cyan'], labelcolor=COLORS['text_primary'],
                 framealpha=0.95, fontsize=9)
        ax.grid(True, alpha=0.15, color=COLORS['text_muted'], linestyle='--', linewidth=0.8)
        ax.tick_params(colors=COLORS['text_primary'], labelsize=9)
        
        for spine in ax.spines.values():
            spine.set_edgecolor(COLORS['border'])
            spine.set_linewidth(1)
        
        canvas = FigureCanvasTkAgg(fig, master=self.right)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
    
    def _export(self):
        if self.current_solution is None:
            messagebox.showwarning("Warning", "Solve first")
            return
        
        d = filedialog.askdirectory(title="Save to:")
        if not d:
            return
        
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            fig, ax = plt.subplots(figsize=(12, 9), facecolor=COLORS['bg_primary'])
            ax.set_facecolor(COLORS['bg_secondary'])
            
            x_range = (0, 8)
            x = np.linspace(*x_range, 300)
            colors_p = ['#ff6b6b', '#4ecdc4', '#ffe66d']
            
            for i, c in enumerate(self.current_solution['constraints']):
                a, b = c['A']
                if abs(b) > 1e-10:
                    y = (c['b'] - a * x) / b
                    ax.plot(x, y, color=colors_p[i], linewidth=2.5)
                    if c['type'] == '>=':
                        ax.fill_between(x, y, 10, alpha=0.1, color=colors_p[i])
                    elif c['type'] == '<=':
                        ax.fill_between(x, 0, y, alpha=0.1, color=colors_p[i])
            
            for v in self.solver.vertices:
                ax.plot(v[0], v[1], 'o', color=COLORS['accent_green'], markersize=9)
            
            ox, oy = self.solver.optimal_point
            ax.plot(ox, oy, marker='*', color=COLORS['accent_gold'], markersize=30,
                   markeredgecolor='white', markeredgewidth=1)
            
            ax.set_xlim(x_range)
            ax.set_ylim(0, 10)
            ax.set_xlabel(f'Portion of {self.current_solution["food1"]}',
                         color=COLORS['text_primary'], fontsize=11, weight='bold')
            ax.set_ylabel(f'Portion of {self.current_solution["food2"]}',
                         color=COLORS['text_primary'], fontsize=11, weight='bold')
            ax.set_title('Graphical Solution', color=COLORS['accent_cyan'], fontsize=13, weight='bold')
            ax.grid(True, alpha=0.2, color=COLORS['text_muted'])
            ax.tick_params(colors=COLORS['text_primary'])
            
            png = os.path.join(d, f"chapter1_{ts}.png")
            fig.savefig(png, dpi=300, bbox_inches='tight', facecolor=COLORS['bg_primary'])
            plt.close(fig)
            
            txt = os.path.join(d, f"chapter1_{ts}.txt")
            with open(txt, 'w') as f:
                f.write("="*70 + "\nCHAPTER 1: GRAPHICAL METHOD RESULTS\n" + "="*70 + "\n\n")
                f.write(f"Minimize: {self.current_solution['c'][0]}·{self.current_solution['food1']} + ")
                f.write(f"{self.current_solution['c'][1]}·{self.current_solution['food2']}\n\n")
                f.write("Constraints:\n")
                for i, c in enumerate(self.current_solution['constraints'], 1):
                    f.write(f"{i}. {c['A'][0]}·{self.current_solution['food1']} + ")
                    f.write(f"{c['A'][1]}·{self.current_solution['food2']} {c['type']} {c['b']}\n")
                f.write("\n" + "-"*70 + "\nOPTIMAL SOLUTION:\n" + "-"*70 + "\n")
                f.write(f"{self.current_solution['food1']}: {self.solver.optimal_point[0]:.4f}\n")
                f.write(f"{self.current_solution['food2']}: {self.solver.optimal_point[1]:.4f}\n")
                f.write(f"Minimum: {self.solver.optimal_value:.2f} kcal\n")
            
            messagebox.showinfo("✓ Success", f"Exported:\n{os.path.basename(png)}\n{os.path.basename(txt)}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")


class Chapter2Tab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.solver = SimplexSolver()
        self.tab_idx = 0
        self.problem = None
        
        # PanedWindow
        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Left
        left_cont = tk.Frame(paned, bg=COLORS['bg_primary'])
        paned.add(left_cont, weight=0)
        
        left_canvas = tk.Canvas(left_cont, bg=COLORS['bg_primary'], highlightthickness=0,
                               borderwidth=0, width=380)
        left_scroll = ttk.Scrollbar(left_cont, orient="vertical", command=left_canvas.yview)
        left_panel = ttk.Frame(left_canvas)
        
        left_panel.bind("<Configure>", lambda e: left_canvas.configure(scrollregion=left_canvas.bbox("all")))
        left_canvas.create_window((0, 0), window=left_panel, anchor="nw")
        left_canvas.configure(yscrollcommand=left_scroll.set)
        left_canvas.pack(side="left", fill="both", expand=True)
        left_scroll.pack(side="right", fill="y")
        
        # Header
        header = tk.Frame(left_panel, bg=COLORS['bg_secondary'], highlightthickness=1,
                         highlightbackground=COLORS['border'])
        header.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(header, text="SIMPLEX ALGORITHM", font=("Segoe UI", 13, "bold"),
                fg=COLORS['accent_cyan'], bg=COLORS['bg_secondary']).pack(pady=8)
        tk.Label(header, text="3-Variable Linear Programming", font=("Segoe UI", 9),
                fg=COLORS['text_secondary'], bg=COLORS['bg_secondary']).pack(pady=(0, 8))
        
        # Sections
        self._create_food_inputs_ch2(left_panel)
        self._create_constraints_ch2(left_panel)
        self._create_buttons_ch2(left_panel)
        self._create_solution_ch2(left_panel)
        
        # Right panel - Tableau display
        self.right = tk.Frame(paned, bg=COLORS['bg_primary'])
        paned.add(self.right, weight=1)
        self._create_tableau_panel(self.right)
        
        self._load_default_ch2()
    
    def _create_food_inputs_ch2(self, parent):
        frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                        highlightbackground=COLORS['border'])
        frame.pack(fill="x", padx=10, pady=(5, 10))
        
        tk.Label(frame, text="🍗 FOODS & OBJECTIVE", font=("Segoe UI", 10, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=10, pady=8)
        
        # Objective sense selector
        obj_row = tk.Frame(frame, bg=COLORS['bg_tertiary'])
        obj_row.pack(fill="x", padx=10, pady=(0, 10))
        tk.Label(obj_row, text="Objective:", font=("Segoe UI", 9, "bold"),
                fg=COLORS['text_primary'], bg=COLORS['bg_tertiary'], width=12).pack(side="left")
        self.objective_sense = ttk.Combobox(obj_row, values=["MIN", "MAX"], width=8, state='readonly')
        self.objective_sense.pack(side="left", padx=5)
        self.objective_sense.set("MIN")
        
        foods_data = [("Chicken", "250"), ("Rice", "200"), ("Vegetables", "150")]
        self.foods_ch2 = []
        
        for name, cal in foods_data:
            row = tk.Frame(frame, bg=COLORS['bg_tertiary'])
            row.pack(fill="x", padx=10, pady=(0, 6))
            
            fn = ttk.Entry(row, width=14)
            fn.pack(side="left", padx=5, fill="x", expand=True)
            fn.insert(0, name)
            
            tk.Label(row, text="kcal:", font=("Segoe UI", 9), fg=COLORS['text_secondary'],
                    bg=COLORS['bg_tertiary']).pack(side="left", padx=(10, 2))
            
            fc = ttk.Entry(row, width=10)
            fc.pack(side="left", padx=2)
            fc.insert(0, cal)
            
            self.foods_ch2.append({'name': fn, 'cal': fc})
    
    def _create_constraints_ch2(self, parent):
        frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                        highlightbackground=COLORS['border'])
        frame.pack(fill="x", padx=10, pady=(5, 10))
        
        tk.Label(frame, text="📋 CONSTRAINTS", font=("Segoe UI", 10, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=10, pady=8)
        
        # Header
        hdr = tk.Frame(frame, bg=COLORS['bg_tertiary'])
        hdr.pack(fill="x", padx=10, pady=(0, 3))
        tk.Label(hdr, text="Name", font=("Segoe UI", 8, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], width=9).pack(side="left", padx=1)
        tk.Label(hdr, text="F1", font=("Segoe UI", 8, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], width=5).pack(side="left", padx=1)
        tk.Label(hdr, text="F2", font=("Segoe UI", 8, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], width=5).pack(side="left", padx=1)
        tk.Label(hdr, text="F3", font=("Segoe UI", 8, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], width=5).pack(side="left", padx=1)
        tk.Label(hdr, text="Type", font=("Segoe UI", 8, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], width=4).pack(side="left", padx=1)
        tk.Label(hdr, text="RHS", font=("Segoe UI", 8, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], width=6).pack(side="left", padx=1)
        
        self.const_ch2 = []
        defaults = [
            ("Proteins", "30", "5", "10", ">=", "60"),
            ("Lipids", "10", "2", "5", "<=", "50"),
            ("Carbs", "0", "40", "20", ">=", "100"),
            ("Fiber", "5", "3", "8", ">=", "30")
        ]
        
        for name, c1, c2, c3, ctype, rhs in defaults:
            row = tk.Frame(frame, bg=COLORS['bg_tertiary'])
            row.pack(fill="x", padx=10, pady=2)
            
            cn = ttk.Entry(row, width=9)
            cn.pack(side="left", padx=1)
            cn.insert(0, name)
            
            ce1 = ttk.Entry(row, width=5)
            ce1.pack(side="left", padx=1)
            ce1.insert(0, c1)
            
            ce2 = ttk.Entry(row, width=5)
            ce2.pack(side="left", padx=1)
            ce2.insert(0, c2)
            
            ce3 = ttk.Entry(row, width=5)
            ce3.pack(side="left", padx=1)
            ce3.insert(0, c3)
            
            ct = ttk.Combobox(row, values=[">=", "<=", "="], width=3, state='readonly')
            ct.pack(side="left", padx=1)
            ct.set(ctype)
            
            cr = ttk.Entry(row, width=6)
            cr.pack(side="left", padx=1)
            cr.insert(0, rhs)
            
            self.const_ch2.append({'name': cn, 'c1': ce1, 'c2': ce2, 'c3': ce3, 'type': ct, 'rhs': cr})
    
    def _create_buttons_ch2(self, parent):
        frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(frame, text="🔍 SOLVE", font=("Segoe UI", 10, "bold"),
                 bg=COLORS['accent_cyan'], fg=COLORS['bg_primary'],
                 activebackground=COLORS['accent_green'], command=self._solve_ch2,
                 padx=12, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=3,
                                                                        fill="both", expand=True)
        
        tk.Button(frame, text="💾 EXPORT", font=("Segoe UI", 10, "bold"),
                 bg=COLORS['accent_gold'], fg=COLORS['bg_primary'],
                 activebackground=COLORS['accent_green'], command=self._export_ch2,
                 padx=12, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=3,
                                                                        fill="both", expand=True)
        
        tk.Button(frame, text="🔄 RESET", font=("Segoe UI", 10, "bold"),
                 bg=COLORS['text_muted'], fg=COLORS['bg_primary'],
                 activebackground=COLORS['accent_green'], command=self._load_default_ch2,
                 padx=12, pady=8, relief="flat", cursor="hand2").pack(side="left", padx=3,
                                                                        fill="both", expand=True)
    
    def _create_solution_ch2(self, parent):
        frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                        highlightbackground=COLORS['border'])
        frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        tk.Label(frame, text="✨ SOLUTION", font=("Segoe UI", 10, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=10, pady=8)
        
        # Solution summary
        self.sol_text_ch2 = tk.Text(frame, height=6, bg=COLORS['bg_secondary'],
                                   fg=COLORS['accent_cyan'], font=('Courier New', 8, 'bold'),
                                   relief="flat", borderwidth=0)
        self.sol_text_ch2.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.sol_text_ch2.configure(state='disabled')
        
        # Transformation display
        trans_frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                              highlightbackground=COLORS['border'])
        trans_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        
        tk.Label(trans_frame, text="🔄 TRANSFORMATIONS", font=("Segoe UI", 9, "bold"),
                fg=COLORS['accent_gold'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=8, pady=6)
        
        self.trans_text = tk.Text(trans_frame, height=4, bg=COLORS['bg_secondary'],
                                 fg=COLORS['accent_gold'], font=('Courier New', 8),
                                 relief="flat", borderwidth=0)
        self.trans_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.trans_text.configure(state='disabled')
    
    def _create_tableau_panel(self, parent):
        """Create tableau display on right panel"""
        # Header
        header = tk.Frame(parent, bg=COLORS['bg_secondary'], highlightthickness=1,
                         highlightbackground=COLORS['border'])
        header.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(header, text="SIMPLEX ITERATIONS", font=("Segoe UI", 13, "bold"),
                fg=COLORS['accent_cyan'], bg=COLORS['bg_secondary']).pack(pady=8)
        
        # Navigation
        nav = tk.Frame(parent, bg=COLORS['bg_primary'])
        nav.pack(fill="x", padx=10, pady=10)
        
        tk.Button(nav, text="◀ PREV", font=("Segoe UI", 9, "bold"),
                 bg=COLORS['accent_cyan'], fg=COLORS['bg_primary'],
                 command=self._prev_tab, padx=8, pady=6, relief="flat", cursor="hand2").pack(side="left", padx=2)
        
        self.tab_label = tk.Label(nav, text="Tableau 0/0", font=("Segoe UI", 10, "bold"),
                                 fg=COLORS['accent_cyan'], bg=COLORS['bg_primary'])
        self.tab_label.pack(side="left", expand=True)
        
        tk.Button(nav, text="NEXT ▶", font=("Segoe UI", 9, "bold"),
                 bg=COLORS['accent_cyan'], fg=COLORS['bg_primary'],
                 command=self._next_tab, padx=8, pady=6, relief="flat", cursor="hand2").pack(side="left", padx=2)
        
        # Info panel for current iteration
        info_frame = tk.Frame(parent, bg=COLORS['bg_tertiary'], highlightthickness=1,
                             highlightbackground=COLORS['border'])
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(info_frame, text="ITERATION INFO", font=("Segoe UI", 9, "bold"),
                fg=COLORS['accent_green'], bg=COLORS['bg_tertiary'], anchor="w").pack(fill="x", padx=8, pady=6)
        
        self.iter_info_text = tk.Text(info_frame, height=3, bg=COLORS['bg_secondary'],
                                      fg=COLORS['accent_green'], font=('Courier New', 8),
                                      relief="flat", borderwidth=0)
        self.iter_info_text.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        self.iter_info_text.configure(state='disabled')
        
        # Tableau display container
        self.tableau_f = tk.Frame(parent, bg=COLORS['bg_primary'])
        self.tableau_f.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    def _load_default_ch2(self):
        self._solve_ch2()
    
    def _solve_ch2(self):
        try:
            # Create fresh solver instance
            self.solver = SimplexSolver()
            
            # Get objective sense
            is_minimization = self.objective_sense.get() == "MIN"
            
            # Get objective coefficients
            c = np.array([float(f['cal'].get()) for f in self.foods_ch2])
            
            # Get constraints
            A_primal = []
            b_primal = []
            constraint_types = []
            transformations = []
            
            for i, e in enumerate(self.const_ch2):
                c1 = float(e['c1'].get())
                c2 = float(e['c2'].get())
                c3 = float(e['c3'].get())
                rhs = float(e['rhs'].get())
                name = e['name'].get()
                ctype = e['type'].get()
                
                constraint_types.append(ctype)
                
                # Convert all constraints to >= form
                if ctype == "<=":
                    # Multiply by -1: <= becomes >=
                    A_primal.append([-c1, -c2, -c3])
                    b_primal.append(-rhs)
                    transformations.append({
                        'original': f"{name}: {c1}·x₁ + {c2}·x₂ + {c3}·x₃ ≤ {rhs}",
                        'transformed': f"{name}: {-c1}·x₁ + {-c2}·x₂ + {-c3}·x₃ ≥ {-rhs}",
                        'reason': "Convert ≤ to ≥"
                    })
                elif ctype == "=":
                    # Keep equality constraints as is (will be split into >= and <=)
                    A_primal.append([c1, c2, c3])
                    b_primal.append(rhs)
                    transformations.append({
                        'original': f"{name}: {c1}·x₁ + {c2}·x₂ + {c3}·x₃ = {rhs}",
                        'transformed': f"{name}: Handled as >= (equality)",
                        'reason': "Equality constraint"
                    })
                else:  # >=
                    A_primal.append([c1, c2, c3])
                    b_primal.append(rhs)
            
            A_primal = np.array(A_primal)
            b_primal = np.array(b_primal)
            
            # Get names
            food_names = [f['name'].get() for f in self.foods_ch2]
            constraint_names = [e['name'].get() for e in self.const_ch2]
            
            # Solve
            self.solver.solve(c, A_primal, b_primal,
                            var_names=food_names,
                            constraint_names=constraint_names,
                            is_minimization=is_minimization)
            
            self.problem = {
                'foods': food_names,
                'c': c,
                'transformations': transformations,
                'objective_sense': 'MIN' if is_minimization else 'MAX'
            }
            
            self.tab_idx = 0
            self._display_tableau(0)
            self._update_solution_ch2()
        except Exception as e:
            import traceback
            messagebox.showerror("Error", f"Error:\n{str(e)}\n\n{traceback.format_exc()}")
    
    def _display_tableau(self, idx):
        # Clear all widgets in tableau frame
        for w in self.tableau_f.winfo_children():
            w.destroy()
        
        if self.solver is None or idx >= len(self.solver.tableaux):
            return
        
        tableau_info = self.solver.tableaux[idx]
        tableau = tableau_info['tableau']
        
        # Get actual variable names from solver (includes slack variables like e1, e2, etc.)
        var_names = self.solver.all_var_names
        
        # Create canvas with scrollbar
        canvas_frame = tk.Frame(self.tableau_f, bg=COLORS['bg_primary'])
        canvas_frame.pack(fill="both", expand=True)
        
        # Scrollbars
        h_scroll = ttk.Scrollbar(canvas_frame, orient="horizontal")
        h_scroll.pack(side="bottom", fill="x")
        
        v_scroll = ttk.Scrollbar(canvas_frame, orient="vertical")
        v_scroll.pack(side="right", fill="y")
        
        # Treeview - use actual variable names
        # Add row label for basis variables
        cols = var_names + ["RHS"]
        tree = ttk.Treeview(canvas_frame, columns=cols, height=10, show='tree headings',
                           yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        
        v_scroll.config(command=tree.yview)
        h_scroll.config(command=tree.xview)
        
        # Set column widths and headings
        tree.column("#0", width=0)  # Hide row number column
        for i, var_name in enumerate(cols):
            col_width = 70 if var_name == "RHS" else 60
            tree.column(var_name, width=col_width, anchor=tk.CENTER)
            # Highlight slack variables (e1, e2, etc.)
            if var_name.startswith('e'):
                tree.heading(var_name, text=var_name)
            elif var_name == "RHS":
                tree.heading(var_name, text="RHS")
            else:
                tree.heading(var_name, text=var_name)
        
        # Insert tableau rows (including Z row at bottom)
        for i in range(tableau.shape[0]):
            row_label = "Z" if i == tableau.shape[0] - 1 else f"C{i+1}"
            values = tuple(f"{tableau[i, j]:.4f}" for j in range(tableau.shape[1]))
            tree.insert('', 'end', text=row_label, values=values)
        
        # Update iteration info
        info = f"Tableau {idx}\n"
        if idx == 0:
            info += f"Initial: Basis = {', '.join(tableau_info['basis_names'])}"
        else:
            info += f"Enter: {tableau_info['entering']}\nLeave: {tableau_info['leaving']}"
            if tableau_info['is_optimal']:
                info += " [OPTIMAL]"
        
        self.iter_info_text.configure(state='normal')
        self.iter_info_text.delete('1.0', tk.END)
        self.iter_info_text.insert('1.0', info)
        self.iter_info_text.configure(state='disabled')
        
        self.tab_label.configure(text=f"Tableau {idx}/{len(self.solver.tableaux)-1}")
    
    def _prev_tab(self):
        if self.tab_idx > 0:
            self.tab_idx -= 1
            self._display_tableau(self.tab_idx)
    
    def _next_tab(self):
        if self.tab_idx < len(self.solver.tableaux) - 1:
            self.tab_idx += 1
            self._display_tableau(self.tab_idx)
    
    def _update_solution_ch2(self):
        sol = self.solver.optimal_solution
        
        # Check if solution is valid
        if self.solver.status == "infeasible":
            txt = f"⚠ NO SOLUTION ({self.problem['objective_sense']})\n\n"
            txt += "The problem is infeasible (no feasible solution exists)."
        elif self.solver.status == "unbounded":
            txt = f"⚠ UNBOUNDED ({self.problem['objective_sense']})\n\n"
            txt += "The problem is unbounded (objective can be improved infinitely)."
        else:
            txt = f"✓ SOLUTION ({self.problem['objective_sense']})\n\n"
            
            for i, food in enumerate(self.problem['foods']):
                if i < len(sol):
                    txt += f"{food}: {sol[i]:.4f}\n"
            
            txt += f"\n{'Minimize' if self.problem['objective_sense'] == 'MIN' else 'Maximize'}: "
            if self.solver.optimal_value is not None and self.solver.optimal_value != float('inf'):
                txt += f"{self.solver.optimal_value:.2f}"
            else:
                txt += "N/A"
        
        txt += f"\nStatus: {self.solver.status}"
        txt += f"\nIterations: {len(self.solver.tableaux)-1}"
        
        self.sol_text_ch2.configure(state='normal')
        self.sol_text_ch2.delete('1.0', tk.END)
        self.sol_text_ch2.insert('1.0', txt)
        self.sol_text_ch2.configure(state='disabled')
        
        # Display transformations
        trans_txt = "PROBLEM SETUP:\n\n"
        
        # Add objective sense info
        if self.problem['objective_sense'] == 'MIN':
            trans_txt += "• Objective: MINIMIZE\n"
            trans_txt += "• Converted to dual: MAXIMIZE\n\n"
        else:
            trans_txt += "• Objective: MAXIMIZE\n\n"
        
        # Add constraint transformations
        if self.problem['transformations']:
            for trans in self.problem['transformations']:
                trans_txt += f"• {trans['reason']}\n"
        else:
            trans_txt += "• No transformations needed\n"
        
        self.trans_text.configure(state='normal')
        self.trans_text.delete('1.0', tk.END)
        self.trans_text.insert('1.0', trans_txt)
        self.trans_text.configure(state='disabled')
    
    def _export_ch2(self):
        if self.problem is None:
            messagebox.showwarning("Warning", "Solve first")
            return
        
        d = filedialog.askdirectory(title="Save to:")
        if not d:
            return
        
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            txt = os.path.join(d, f"chapter2_{ts}.txt")
            
            with open(txt, 'w') as f:
                f.write("="*70 + "\nCHAPTER 2: SIMPLEX METHOD RESULTS\n" + "="*70 + "\n\n")
                f.write("TABLEAUX ITERATIONS:\n\n")
                
                for i, tab in enumerate(self.solver.tableaux):
                    f.write(f"Tableau {i}:\n")
                    f.write(str(tab) + "\n\n")
                
                f.write("-"*70 + "\nOPTIMAL SOLUTION:\n" + "-"*70 + "\n")
                for i, food in enumerate(self.problem['foods']):
                    f.write(f"{food}: {self.solver.optimal_solution[i]:.4f}\n")
                f.write(f"Minimum: {self.solver.optimal_value:.2f} kcal\n")
            
            messagebox.showinfo("✓ Success", f"Exported:\n{os.path.basename(txt)}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")
