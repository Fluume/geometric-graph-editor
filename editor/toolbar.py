import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
import sys
import graph_generator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""Explication : 
    Cette ligne ajoute le répertoire parent du script actuel au chemin de recherche des modules Python.
    Cela permet d'importer des modules qui se trouvent dans le répertoire parent.
"""

from core.constants import *

# Graphes
from core.algorithms.unit_disk_graph import UnitDiskGraph
from core.algorithms.nearest_neighbor_graph import NearestNeighbourGraph
from core.algorithms.theta_graph import ThetaGraph
from core.algorithms.yao_graph import YaoGraph
from core.algorithms.integer_graph import IntegerGraph
from core.algorithms.relative_neighborhood_graph import RelativeNeighborhoodGraph
from core.algorithms.triangulation_of_delaunay_graph import TriangulationOfDelaunayGraph
from core.algorithms.gabriel_graph import GabrielGraph
from core.algorithms.k_closest_neighbor_graph import KClosestNeighborGraph


from core.graph import Graph


class Toolbar:
    """
    Classe pour créer une barre d'outils (toolbox) à droite de la fenêtre principale.
    Elle contient des boutons et d'autres éléments d'interface utilisateur.
    """

    def __init__(self, root, graph, menu):
        self.canvas = None  # Référence au canvas (zone de dessin) dans la fenêtre principale
        self.menu = menu # Référence au menu de la fenêtre principale
        self.selected_graph_type = "None"  # Type de graphe sélectionné dans la barre d'outils
        # Création d'un panneau (Frame) pour contenir les boutons à droite
        self.frame = tk.Frame(root, background="#d4d4d4", width=400)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame.pack_propagate(False)
        
        self.selected_vertex_index = None  # Variable pour stocker le sommet sélectionné
        self.graph = graph  # Instance de la classe Graph

        # Titre "Toolbox"
        self.label = tk.Label(self.frame, text="Toolbox", font=("Arial", 14), background="#d4d4d4")

        self.settings_label_frame = tk.LabelFrame(self.frame, text="Graph Settings", font=("Arial", 14), background="#d4d4d4")
        self.settings_label_frame.pack(side=tk.TOP, pady=5, fill="both")

        """-------------------ELEMENTS-------------------"""

        # Liste des types de graphes
        self.graph_type_label = tk.Label(self.settings_label_frame, text="Graph Type:", background="#d4d4d4")
        self.graph_type_label.pack(pady=5)

        self.graph_types_combobox = ttk.Combobox(self.settings_label_frame, values = list(graph_types.keys()), width=40)
        self.graph_types_combobox.bind("<<ComboboxSelected>>", self.on_graph_type_select)
        self.graph_types_combobox.current(0)
        self.graph_types_combobox.pack(pady=5)
        
        # Description du type de graphe
        self.graph_type_description = tk.Label(self.settings_label_frame, text="Graph Type Description:", background="#d4d4d4")
        self.graph_type_description.pack(pady=5)

        # Zone de texte pour afficher la description du type de graphe
        self.graph_type_description_text = tk.Text(self.settings_label_frame, height=5, width=40)
        self.graph_type_description_text.pack(pady=5)
        self.graph_type_description_text.insert(tk.END, graph_types[self.selected_graph_type])
        self.graph_type_description_text.config(state="disabled") # Rendre la zone de texte non modifiable
        
        """---------------------GRAPH PARTICULARITIES---------------------"""
        self.graph_type_particularities = tk.Label(self.settings_label_frame, text="Graph Particularities:", background="#d4d4d4")
        self.graph_type_particularities.pack(pady=5)

        self.particularities_frame = tk.Frame(self.settings_label_frame, background="#d4d4d4")
        self.particularities_frame.pack(pady=5)
        self.show_graph_particularities()

        """---------------------GRAPH MANAGEMENT---------------------"""
        self.management_label_frame = tk.LabelFrame(self.frame, text="Graph Management", font=("Arial", 14), background="#d4d4d4")
        self.management_label_frame.pack(side=tk.TOP, pady=5, fill="both")
        # Liste des sommets
        self.vertex_label = tk.Label(self.management_label_frame, text="Vertices:", background="#d4d4d4")
        self.vertex_label.pack(pady=5)
        
        self.vertex_listbox = tk.Listbox(self.management_label_frame, width=30, height=10)
        self.vertex_listbox.pack(pady=5)
        for i in range(graph.get_length()):
            self.vertex_listbox.insert(tk.END, f"{i + 1} | {graph.get_vertex_by_index(i)}")

        self.vertex_listbox.bind("<<ListboxSelect>>", self.on_vertex_select)

        # Bouton pour supprimer un sommet
        self.delete_selected_vertex_button = tk.Button(self.management_label_frame, text="Delete Vertex", command=self.delete_selected_vertex)
        self.delete_selected_vertex_button.pack(pady=5)
        # Bouton pour tout supprimer
        self.delete_all_button = tk.Button(self.management_label_frame, text="Delete All", command=self.delete_all)
        self.delete_all_button.pack(pady=5) 

        # Génération d'un graphe aléatoire
        self.generate_random_graph_button = tk.Button(self.management_label_frame, text="Generate Random Graph", command=self.generate_random_graph_click)
        self.generate_random_graph_button.pack(pady=5)
        """----------------------------------------------------------"""

    def generate_random_graph_click(self):
        """
        Ouvre une fenêtre pour définir le random graph.
        """
        generate_window = tk.Toplevel()
        generate_window.title("Generate Random Graph")
        generate_window.geometry("300x300")
        generate_window.configure(background="#d4d4d4")
        generate_window.resizable(False, False)
        
        # Nombre de points
        num_points_frame = tk.Frame(generate_window, background="#d4d4d4")
        num_points_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.num_points_label = tk.Label(num_points_frame, text="Number of Points:", background="#d4d4d4")
        self.num_points_label.pack(side=tk.LEFT, padx=5)
        self.num_points_scale = tk.Scale(num_points_frame, from_=0, to=1000, orient=tk.HORIZONTAL, background="#d4d4d4",width= 10)
        self.num_points_scale.pack(side=tk.RIGHT, padx=5)
        self.num_points_scale.set(100) 

        # X min
        x_min_frame = tk.Frame(generate_window, background="#d4d4d4")
        x_min_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.x_min_label = tk.Label(x_min_frame, text="X min:", background="#d4d4d4")
        self.x_min_label.pack(side=tk.LEFT, padx=5)
        self.x_min_scale = tk.Scale(x_min_frame, from_=0, to=800, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.x_min_scale.pack(side=tk.RIGHT, padx=5)
        self.x_min_scale.set(0) 

        # X max
        x_max_frame = tk.Frame(generate_window, background="#d4d4d4")
        x_max_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.x_max_label = tk.Label(x_max_frame, text="X max:", background="#d4d4d4")
        self.x_max_label.pack(side=tk.LEFT, padx=5)
        self.x_max_scale = tk.Scale(x_max_frame, from_=0, to=800, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.x_max_scale.pack(side=tk.RIGHT, padx=5)
        self.x_max_scale.set(800)

        # Y min
        y_min_frame = tk.Frame(generate_window, background="#d4d4d4")
        y_min_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.y_min_label = tk.Label(y_min_frame, text="Y min:", background="#d4d4d4")
        self.y_min_label.pack(side=tk.LEFT, padx=5)
        self.y_min_scale = tk.Scale(y_min_frame, from_=0, to=800, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.y_min_scale.pack(side=tk.RIGHT, padx=5)
        self.y_min_scale.set(0)

        # Y max
        y_max_frame = tk.Frame(generate_window, background="#d4d4d4")
        y_max_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.y_max_label = tk.Label(y_max_frame, text="Y max:", background="#d4d4d4")
        self.y_max_label.pack(side=tk.LEFT, padx=5)
        self.y_max_scale = tk.Scale(y_max_frame, from_=0, to=800, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.y_max_scale.pack(side=tk.RIGHT, padx=5)
        self.y_max_scale.set(800)

        # Label pour plus de précision
        self.more_precision_label = tk.Label(generate_window, text="For more precision, use the command line", background="#d4d4d4")
        self.more_precision_label.pack(pady=5)

        # Bouton générer
        self.generate_button = tk.Button(generate_window, text="Generate", command=self.on_generate_random_graph)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        

    def on_generate_random_graph(self):
        # Vérification des valeurs
        num_points = self.num_points_scale.get()
        x_min = self.x_min_scale.get()
        x_max = self.x_max_scale.get()
        y_min = self.y_min_scale.get()
        y_max = self.y_max_scale.get()

        if num_points <= 0 or x_min >= x_max or y_min >= y_max:
            messagebox.showerror("Error", "Invalid coordinate ranges.")
            return
        
        # Génération du graphe aléatoire
        new_graph = graph_generator.generate_random_graph(num_points, x_min, x_max, y_min, y_max)
        self.select_graph_type(NONE_GRAPH)  # Sélectionner le type de graphe "Simple Graph"
        self.graph.vertices = new_graph.vertices  # Mettre à jour le graphe dans la barre d'outils
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas
        self.update_vertex_list(self.graph)  # Mettre à jour la liste des sommets dans la barre d'outils


    def update_radius(self):
        self.unit_disk_graph_radius.set(self.graph.radius)


    def show_graph_particularities(self):
        # Vider le contenu du frame des particularités
        for widget in self.particularities_frame.winfo_children():
            widget.destroy()

        # Rien à afficher si le type de graphe est "None"
        if self.selected_graph_type == UNIT_DISK_GRAPH:
            self.unit_disk_graph_radius = tk.Scale(self.particularities_frame, from_=0, to=200, orient=tk.HORIZONTAL, label="Radius", background="#d4d4d4", command=self.on_radius_change)
            self.update_radius()
            self.unit_disk_graph_radius.pack(pady=5)
            self.show_circle = tk.Checkbutton(self.particularities_frame, text="Show Circles", background="#d4d4d4", command = self.on_circle_check)
            self.show_circle.pack(pady=5)
        elif self.selected_graph_type == THETA_GRAPH:
            self.projection_angle = tk.Scale(self.particularities_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Projection Angle percentage", background="#d4d4d4", command=self.on_projection_angle_change)
            self.projection_angle.pack(pady=5)
            self.projection_angle.set(50)
            self.k_scale = tk.Scale(self.particularities_frame, from_=2, to=12, orient=tk.HORIZONTAL, label="Number of sectors (K)", background="#d4d4d4", command=self.on_number_of_sectors_change)
            self.k_scale.pack(pady=5)
            self.k_scale.set(6)
        elif self.selected_graph_type == YAO_GRAPH:
            self.k_scale = tk.Scale(self.particularities_frame, from_=2, to=12, orient=tk.HORIZONTAL, label="Number of sectors (K)", background="#d4d4d4", command=self.on_number_of_sectors_change)
            self.k_scale.pack(pady=5)
            self.k_scale.set(6)
        elif self.selected_graph_type == INTEGER_GRAPH or self.selected_graph_type == RELATIVE_NEIGHBORHOOD_GRAPH:
            self.show_distance = tk.Checkbutton(self.particularities_frame, text="Show Distance", background="#d4d4d4", command = self.on_show_distance_check)
            self.show_distance.pack(pady=5)
            if self.canvas.show_distance:
                self.show_distance.select()
        elif self.selected_graph_type == TRIANGULATION_OF_DELAUNAY_GRAPH:
            self.show_circle = tk.Checkbutton(self.particularities_frame, text="Show Circles", background="#d4d4d4", command = self.on_delaunay_circle_check)
            self.show_circle.pack(pady=5)
            if self.canvas.show_circle_delaunay_graph:
                self.show_circle.select()
        elif self.selected_graph_type == K_CLOSEST_NEIGHBORS_GRAPH:
            self.k_scale = tk.Scale(self.particularities_frame, from_=1, to=10, orient=tk.HORIZONTAL, label="Number of neighbors (K)", background="#d4d4d4", command=self.on_neighbor_change)
            self.k_scale.pack(pady=5)
            self.k_scale.set(1)
                

        # Rien à afficher si le type de graphe est NEAREST_NEIGHBOR_GRAPH

    """------------------K CLOSEST NEIGHBOR-----------------"""
    def on_neighbor_change(self, value):
        self.graph.set_k(int(value))
        self.canvas.display_graph(self.graph)

    """------------------DELAUNAY GRAPH-----------------"""
    def on_delaunay_circle_check(self):
        self.canvas.show_circle_delaunay_graph = not self.canvas.show_circle_delaunay_graph
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas
    

    """------INTEGER / RELATIVE NEIGHBORHOOD GRAPH------"""
    def on_show_distance_check(self):
        self.canvas.show_distance = not self.canvas.show_distance
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

    """------THETA / YAO GRAPH------"""
    def on_projection_angle_change(self, value):
        """
        Gère le changement de valeur du paramètre K pour le graphe Theta.
        :param value: Nouvelle valeur de K.
        """
        self.graph.set_projection_angle_percent(int(value) / 100)
        self.canvas.display_graph(self.graph)

    def on_number_of_sectors_change(self, value):
        """
        Gère le changement de valeur du paramètre K pour le graphe Theta.
        :param value: Nouvelle valeur de K.
        """
        self.graph.set_sectors(int(value))
        self.canvas.display_graph(self.graph)

    """"------UNIT DISK GRAPH------"""
    def on_circle_check(self):
        self.canvas.show_circle_unit_disk_graph = not self.canvas.show_circle_unit_disk_graph  # Inverser l'état de l'affichage des cercles
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

    def on_radius_change(self, value):
        self.graph.set_radius(int(value))  # Mettre à jour le rayon du graphe de disque unitaire
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas
    """----------------------------"""

    def delete_all(self):
        """
        Supprime tous les sommets du graphe et met à jour la liste des sommets dans la barre d'outils.
        """
        self.graph.vertices.clear()
        self.graph.linked_points.clear()
        self.vertex_listbox.delete(0, tk.END)  # Effacer la liste des sommets
        self.selected_vertex_index = None  # Réinitialiser l'index du sommet sélectionné
        self.update_vertex_list(self.graph)  # Mettre à jour la liste des sommets dans la barre d'outils
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

    def delete_selected_vertex(self):
        """
        Supprime le sommet sélectionné dans la liste et le graphe.
        """
        if self.selected_vertex_index == None: return
        print(f"Deleting vertex {self.selected_vertex_index}")
        # Supprimer le sommet du graphe
        self.graph.remove_vertex(self.graph.get_vertex_by_index(self.selected_vertex_index))
        self.selected_vertex_index = None  # Réinitialiser l'index du sommet sélectionné
        self.update_vertex_list(self.graph)
        self.canvas.display_graph(self.graph)
 
    def on_graph_type_select(self, event):
        self.selected_graph_type = self.graph_types_combobox.get()

        # remove graph desc test
        self.graph_type_description_text.config(state="normal")
        self.graph_type_description_text.delete("1.0", tk.END)
        self.graph_type_description_text.insert(tk.END, graph_types[self.selected_graph_type])
        self.graph_type_description_text.config(state="disabled")
        print(f"Selected graph type: {self.selected_graph_type}")
        
        if self.selected_graph_type == UNIT_DISK_GRAPH:
            self.graph = UnitDiskGraph(self.graph.vertices)
        elif self.selected_graph_type == NEAREST_NEIGHBOR_GRAPH:
            self.graph = NearestNeighbourGraph(self.graph.vertices)
        elif self.selected_graph_type == THETA_GRAPH:
            self.graph = ThetaGraph(self.graph.vertices)
        elif self.selected_graph_type == YAO_GRAPH:
            self.graph = YaoGraph(self.graph.vertices)
        elif self.selected_graph_type == INTEGER_GRAPH:
            self.graph = IntegerGraph(self.graph.vertices)
        elif self.selected_graph_type == RELATIVE_NEIGHBORHOOD_GRAPH:
            self.graph = RelativeNeighborhoodGraph(self.graph.vertices)
        elif self.selected_graph_type == TRIANGULATION_OF_DELAUNAY_GRAPH:
            self.graph = TriangulationOfDelaunayGraph(self.graph.vertices)
        elif self.selected_graph_type == GABRIEL_GRAPH:
            self.graph = GabrielGraph(self.graph.vertices)
        elif self.selected_graph_type == K_CLOSEST_NEIGHBORS_GRAPH:
            self.graph = KClosestNeighborGraph(self.graph.vertices)
        else:
            self.graph = Graph(vertices = self.graph.vertices)

        self.show_graph_particularities()  # Afficher les particularités du graphe sélectionné
        
        self.canvas.graph = self.graph  # Mettre à jour la référence du graphe dans le canvas
        self.menu.graph = self.graph  # Mettre à jour la référence du graphe dans le menu
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

    def select_graph_type(self, graph_type):
        """
        Sélectionne le type de graphe dans la barre d'outils.
        :param graph_type: Type de graphe à sélectionner.
        """
        self.selected_graph_type = graph_type
        self.graph_types_combobox.set(graph_type)
        self.on_graph_type_select(None)  # Appeler la méthode de sélection de type de graphe pour mettre à jour l'affichage

    def update_vertex_list(self, graph):
        """
        Met à jour la liste des sommets dans la barre d'outils.
        :param vertices: Liste des sommets à afficher.
        """
        self.vertex_listbox.delete(0, tk.END)
        for i in range(graph.get_length()):
            self.vertex_listbox.insert(tk.END, f"{i + 1} | {graph.get_vertex_by_index(i)}")
    
    def on_vertex_select(self, event, vertex = None):
        """
        Gère l'événement de sélection d'un sommet dans la liste ou dans le graph.
        :param event: Événement de sélection.
        :param vertex: Sommet sélectionné (dans le cas de la sélection du sommet depuis le canvas).
        """
        if len(self.vertex_listbox.curselection()) == 0:
            # Si aucun sommet n'est sélectionné dans la liste, on ne fait rien
            self.selected_vertex_index = vertex
            return
        else:
            self.selected_vertex_index = self.vertex_listbox.curselection()[0] if vertex is None else vertex
        
        
        
        self.canvas.display_graph(self.graph)

    def get_selected_vertex_index(self):
        """
        Retourne le sommet sélectionné dans la liste.
        :return: Coordonnées du sommet sélectionné.
        """
        return self.selected_vertex_index