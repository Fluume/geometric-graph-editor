import tkinter as tk
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # TODO : expliquer
from core.algorithms.unit_disk_graph import UnitDiskGraph

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

        self.dragged_vertex = None  # Variable pour stocker le sommet en cours de drag and drop

        """GRAPH DISPLAYING VARIABLES"""
        # Unit Disk Graph
        self.show_circle_unit_disk_graph = False



    def display_graph(self, graph):
        """
        Affiche le graphe sur le canvas.
        :param graph: Instance de la classe Graph à afficher.
        """
        
        self.canvas.delete("all")
        # Affichage des arêtes
        for edge in graph.linked_points:
            x1, y1 = edge[0][0], edge[0][1]
            x2, y2 = edge[1][0], edge[1][1]
            self.canvas.create_line(x1, y1, x2, y2, fill="black")
        # Affichage des sommets
        for i in range(graph.get_length()):
            vertex = graph.get_vertex_by_index(i)
            x, y = vertex[0], vertex[1]
            color = "blue" if self.toolbar.get_selected_vertex_index() == i else "red"
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill=color)

        """GRAPH PARTICULARITIES"""
        # Unit Disk Graph
        if self.show_circle_unit_disk_graph and isinstance(graph, UnitDiskGraph):
            for vertex in graph.vertices:
                x, y = vertex[0], vertex[1]
                self.canvas.create_oval(x - graph.radius, y - graph.radius, x + graph.radius, y + graph.radius, outline="green", width=1)

    def on_drag_motion(self, event):
        """
        Gère le mouvement de la souris lorsque l'utilisateur fait drag un sommet.
        """
        if self.dragged_vertex:
            # Assure que le sommet est à l'intérieur du canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            x = max(0, min(event.x, canvas_width)) # Limite la position x à l'intérieur du canvas
            y = max(0, min(event.y, canvas_height)) # Idem pour y

            self.graph.remove_vertex(self.dragged_vertex)
            self.graph.add_vertex((x, y))
            self.dragged_vertex = (x, y)  
            self.toolbar.on_vertex_select(event = None, vertex_format = self.graph.vertices.index(self.dragged_vertex))  # Met à jour l'index du sommet sélectionné dans la barre d'outils

            self.toolbar.update_vertex_list(self.graph) 
            self.display_graph(self.graph)


    def on_drag_end(self, event):
        """
        Gère la fin du drag d'un sommet.
        """
        if self.dragged_vertex:
            print(f"Finished dragging vertex to: ({event.x}, {event.y})")
            self.dragged_vertex = None
            self.toolbar.update_vertex_list(self.graph)  

    def on_canvas_left_click(self, event):
        """
        Gère l'événement de clic de souris sur le canvas.
        :param event: Événement de clic de souris.
        """
        x, y = event.x, event.y
    
        closest = self.get_closest_vertex(self.graph, (x, y), 5) # Vérifie si il y a clic sur un sommet

        if closest:
            self.dragged_vertex = closest
            self.toolbar.on_vertex_select(event = None, vertex_format = self.graph.vertices.index(closest))  # Met à jour l'index du sommet sélectionné dans la barre d'outils
            if self.dragged_vertex:
                print(f"Started dragging vertex at: {self.dragged_vertex}")
            
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
        x, y = event.x, event.y
        closest = self.get_closest_vertex(self.graph, (x, y), 10)
        if closest: 
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