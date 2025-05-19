import tkinter as tk
import os
import sys
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
"""Explication : 
    Cette ligne ajoute le répertoire parent du script actuel au chemin de recherche des modules Python.
    Cela permet d'importer des modules qui se trouvent dans le répertoire parent.
"""

from core.algorithms.unit_disk_graph import UnitDiskGraph
from core.algorithms.theta_graph import ThetaGraph
from core.algorithms.yao_graph import YaoGraph
from core.algorithms.integer_graph import IntegerGraph
from core.algorithms.relative_neighborhood_graph import RelativeNeighborhoodGraph
from core.algorithms.triangulation_of_delaunay_graph import TriangulationOfDelaunayGraph



class Canvas:
    """
    Classe pour créer un canvas dans la fenêtre principale.
    Elle permet de dessiner un graphe à la main avec la souris.
    """

    def __init__(self, root, graph, toolbar):
        self.toolbar = toolbar  # Instance de la classe Toolbar
        self.graph = graph  # Instance de la classe Graph
       
        # Frame pour le canvas et son titre
        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Titre "Canvas"
        self.label = tk.Label(self.frame, text="Graph visualisation", font=("Arial", 14))
        self.label.pack(side=tk.TOP, pady=5)

        # Canvas
        self.canvas = tk.Canvas(self.frame, background="#f0f0f0")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.on_canvas_left_click)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_end)
        # Flèches directionnelles
        root.bind("<Up>", self.move_up) 
        root.bind("<Down>", self.move_down)
        root.bind("<Left>", self.move_left)
        root.bind("<Right>", self.move_right)
        # Molette
        root.bind("<MouseWheel>", self.zoom) # Scroll vers le haut ou le bas


        self.dragged_vertex = None  # Variable pour stocker le sommet en cours de drag and drop
        
        self.vertices_offset = (0, 0)  # Décalage des sommets
        self.scale_factor = 1.0  # Facteur d'échelle pour le zoom
        self.vertices_display = []  # Variable pour stocker les sommets affichés
        self.linked_points_display = []  # Variable pour stocker les arêtes affichées

        """GRAPH DISPLAYING VARIABLES"""
        # Unit Disk Graph
        self.show_circle_unit_disk_graph = False
        self.show_distance = False
        self.show_circle_delaunay_graph = False

    def move_offset(self, dx, dy):
        """
        Déplace le graphe sur le canvas en fonction des flèches directionnelles.
        :param dx: Décalage en x.
        :param dy: Décalage en y.
        """
        self.vertices_offset = (self.vertices_offset[0] + dx, self.vertices_offset[1] + dy)
        self.display_graph(self.graph)
    
    def move_up(self, event):
        self.move_offset(0, 5)

    def move_down(self, event):
        self.move_offset(0, -5)

    def move_left(self, event):
        self.move_offset(5, 0)

    def move_right(self, event):
        self.move_offset(-5, 0)

    def zoom(self, event):
        """
        Gère le zoom du canvas avec la molette de la souris.
        :param event: Événement de la molette de la souris.
        """
        self.scale_factor += 0.1 if event.delta > 0 else -0.1
        self.display_graph(self.graph)

    def calculate_display_values(self):
        """
        Calcule les valeurs d'affichage pour le graphe.
        :return: None
        """
        # Calculer les valeurs d'affichage ici si nécessaire
        self.vertices_display = []
        self.linked_points_display = []

        offset_x = self.vertices_offset[0]
        offset_y = self.vertices_offset[1]

        scale = self.scale_factor

        for vertex in self.graph.vertices:
            x, y = (vertex[0] + offset_x) * scale , (vertex[1] + offset_y) * scale
            self.vertices_display.append((x, y))
        
        for edge in self.graph.linked_points:
            x1, y1 = (edge[0][0] + offset_x) * scale, (edge[0][1] + offset_y) * scale
            x2, y2 = (edge[1][0] + offset_x) * scale, (edge[1][1] + offset_y) * scale
            self.linked_points_display.append(((x1, y1), (x2, y2)))

    def display_graph(self, graph):
        """
        Affiche le graphe sur le canvas.
        :param graph: Instance de la classe Graph à afficher.
        """
        self.calculate_display_values()

        n = graph.get_length()

        self.canvas.delete("all")
        # Affichage des arêtes
        for edge in self.linked_points_display:
            x1, y1 = edge[0][0], edge[0][1]
            x2, y2 = edge[1][0], edge[1][1]

            self.canvas.create_line(x1, y1, x2, y2, fill="black")

        # Affichage des sommets
        for i in range(n):
            vertex = self.vertices_display[i]
            x, y = vertex[0], vertex[1]
            color = "blue" if self.toolbar.get_selected_vertex_index() == i else "red"
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color)

        """GRAPH PARTICULARITIES"""
        self.display_graph_particularities(graph)

    def display_graph_particularities(self, graph):
        n = graph.get_length()
        # Unit Disk Graph
        if self.show_circle_unit_disk_graph and isinstance(graph, UnitDiskGraph):
            for vertex in self.vertices_display:
                x, y = vertex[0], vertex[1]
                self.canvas.create_oval(x - graph.radius, y - graph.radius, x + graph.radius, y + graph.radius, outline="green", width=1)
        if isinstance(graph, ThetaGraph) and self.toolbar.get_selected_vertex_index() is not None:
            # Dessiner les secteurs pour le sommet sélectionné
            selected_vertex = self.vertices_display[self.toolbar.get_selected_vertex_index()]

            x, y = selected_vertex[0], selected_vertex[1]
            for i in range(graph.sectors):
                # Cones autour du sommet sélectionné
                theta = (2 * math.pi) / graph.sectors * i 
                self.canvas.create_line(x, y, x + math.cos(theta) * 200, y + math.sin(theta) * 200, fill="green", width=3)
                # Ligne de projection
                theta_proj = (2 * math.pi) / graph.sectors * (i + self.graph.projection_angle_percent)
                self.canvas.create_line(x, y, x + math.cos(theta_proj) * 200, y + math.sin(theta_proj) * 200, fill="red", width=1)
        if isinstance(graph, YaoGraph) and self.toolbar.get_selected_vertex_index() is not None:
            # Dessiner les secteurs pour le sommet sélectionné
            selected_vertex = self.vertices_display[self.toolbar.get_selected_vertex_index()]
            x, y = selected_vertex[0], selected_vertex[1]
            for i in range(graph.sectors):
                # Cones autour du sommet sélectionné
                theta = (2 * math.pi) / graph.sectors * i 
                self.canvas.create_line(x, y, x + math.cos(theta) * 200, y + math.sin(theta) * 200, fill="green", width=3)
        if (isinstance(graph, IntegerGraph) or isinstance(graph, RelativeNeighborhoodGraph)) and self.show_distance:
            for i in range(n):
                for j in range(i + 1, n):
                    # Distance entre les sommets
                    distance = self.graph.distance(self.vertices_display[i], self.vertices_display[j])
                    mid_location = ((self.vertices_display[i][0] + self.vertices_display[j][0]) / 2, (self.vertices_display[i][1] + self.vertices_display[j][1]) / 2)
                    self.canvas.create_text(mid_location[0], mid_location[1], text=str(distance), fill="black") # Affichage de la distance entre les sommets

                    self.canvas.create_line(self.vertices_display[i][0], self.vertices_display[i][1], self.vertices_display[j][0], self.vertices_display[j][1], fill="blue", dash=(2, 2)) # Lignes en pointillés entre les sommets liés par une distance entière
        if isinstance(graph, TriangulationOfDelaunayGraph) and self.show_circle_delaunay_graph and n > 2:
            for i in range(n):
                for j in range(i + 1, n):
                    for k in range(j + 1, n):
                        # Dessiner le cercle passant par les trois sommets
                        center = self.graph.mid_point(self.vertices_display[i], self.vertices_display[j], self.vertices_display[k])
                        if center is not None:
                            radius = self.graph.distance(center, self.vertices_display[i])
                            x, y = center[0], center[1]
                            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline="blue", width=1, dash=(2, 2)) 
                

    def on_drag_motion(self, event):
        """
        Gère le mouvement de la souris lorsque l'utilisateur fait drag un sommet.
        """
        if self.dragged_vertex:
            x = (event.x - self.vertices_offset[0]) / self.scale_factor
            y = (event.y - self.vertices_offset[1]) / self.scale_factor
        
            self.graph.remove_vertex(self.dragged_vertex)
            self.graph.add_vertex((x, y))
            self.dragged_vertex = (x, y)  
            self.toolbar.on_vertex_select(event = None, vertex = self.graph.vertices.index(self.dragged_vertex))  # Met à jour l'index du sommet sélectionné dans la barre d'outils

            self.toolbar.update_vertex_list(self.graph) 
            self.display_graph(self.graph)

    def on_drag_end(self, event):
        """
        Gère la fin du drag d'un sommet.
        """
        if self.dragged_vertex:
            self.dragged_vertex = None
            self.toolbar.update_vertex_list(self.graph)

    def on_canvas_left_click(self, event):
        """
        Gère l'événement de clic de souris sur le canvas.
        :param event: Événement de clic de souris.
        """
        x = (event.x - self.vertices_offset[0]) / self.scale_factor
        y = (event.y - self.vertices_offset[1]) / self.scale_factor

        closest = self.get_closest_vertex(self.graph, (x, y), 5) # Vérifie si il y a clic sur un sommet

        if closest:
            self.dragged_vertex = closest
            self.toolbar.on_vertex_select(event = None, vertex = self.graph.vertices.index(closest))  # Met à jour l'index du sommet sélectionné dans la barre d'outils
            
        else:
            print("Adding vertex at:", (x, y))
            self.graph.add_vertex((x, y))

        self.display_graph(self.graph)
        self.toolbar.update_vertex_list(self.graph)
    
    def on_canvas_right_click(self, event):
        """
        Gère l'événement de clic de souris sur le canvas.
        :param event: Événement de clic de souris.
        """
        x = (event.x - self.vertices_offset[0]) / self.scale_factor
        y = (event.y - self.vertices_offset[1]) / self.scale_factor

        closest = self.get_closest_vertex(self.graph, (x, y), 10)
        if closest and self.dragged_vertex != closest:
            print("Removing vertex at:", closest)
            self.graph.remove_vertex(closest)
            self.display_graph(self.graph)
            self.toolbar.update_vertex_list(self.graph)


    
    def get_closest_vertex(self, graph, coord, threshold):
        """
        Trouve le sommet le plus proche d'un point donné dans le graphe.
        :param graph: Instance de la classe Graph.
        :param coord: Coordonnées du point (x, y).
        :param threshold: Distance maximale pour considérer un sommet comme "proche".
        :return: Le sommet le plus proche ou None si aucun sommet n'est trouvé.
        """
        closest_vertex = None
        min_distance = float("inf")

        for vertex in graph.vertices:
            distance = ((vertex[0] - coord[0]) ** 2 + (vertex[1] - coord[1]) ** 2) ** 0.5
            if distance < min_distance and distance < threshold:
                min_distance = distance
                closest_vertex = vertex

        return closest_vertex