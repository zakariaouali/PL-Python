"""
Main entry point for the Personalized Food Optimization System
Author: Zakaria Ait Ahmad Ouali, Mohammed Amine Mourrane, Aya Benohoud, Mohammed Taha Aboundir
Supervisors: Abdelati REHA & Yassine SAFSOUF
Year: 2025-2026
"""

import tkinter as tk
from gui import FoodOptimizationApp

def main():
    root = tk.Tk()
    app = FoodOptimizationApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
