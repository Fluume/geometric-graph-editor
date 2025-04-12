import tkinter as tk
import os
import sys

from toolbar import Toolbar
from canvas import Canvas
# importation des modules du core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # TODO : expliquer
from core.graph import Graph

graph = Graph()
"""----------------------WINDOW-----------------------"""
resolution = (1200, 800)
root = tk.Tk() # Création de la fenêtre racine
root.title("Geometric Graph Editor V0.1 (" + str(resolution[0]) + "x" + str(resolution[1]) + ")")
root.geometry(str(resolution[0]) + "x" + str(resolution[1]))  # Largeur x Hauteur
root.resizable(False, False)

"""----------------------TOOLBAR----------------------"""
toolbar = Toolbar(root, graph) 
"""----------------------CANVAS-----------------------"""
canvas = Canvas(root, graph, toolbar)
toolbar.canvas = canvas  # Passer la référence du canvas à la barre d'outils

"""----------------------MENU-------------------------"""
"""----------------------GRAPH------------------------"""
canvas.display_graph(graph)  # Affiche le graphe sur le canvas

root.mainloop()  # Boucle principale pour afficher la fenêtre