import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import os
import sys
import random_graph_generator

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # TODO : expliquer

from core.constants import *
from core.algorithms.unit_disk_graph import UnitDiskGraph
from core.algorithms.nearest_neighbor_graph import NearestNeighbourGraph
from core.algorithms.triangulation_of_delaunay import Delaunay_graph
from core.algorithms.gabriel_graph import GabrielGraph
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

        # Number of points
        num_points_frame = tk.Frame(generate_window, background="#d4d4d4")
        num_points_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.num_points_label = tk.Label(num_points_frame, text="Number of Points:", background="#d4d4d4")
        self.num_points_label.pack(side=tk.LEFT, padx=5)
        self.num_points_scale = tk.Scale(num_points_frame, from_=0, to=1000, orient=tk.HORIZONTAL, background="#d4d4d4",width= 10)
        self.num_points_scale.pack(side=tk.RIGHT, padx=5)
        self.num_points_scale.set(100)  # Default value

        # X min
        x_min_frame = tk.Frame(generate_window, background="#d4d4d4")
        x_min_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.x_min_label = tk.Label(x_min_frame, text="X min:", background="#d4d4d4")
        self.x_min_label.pack(side=tk.LEFT, padx=5)
        self.x_min_scale = tk.Scale(x_min_frame, from_=0, to=1000, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.x_min_scale.pack(side=tk.RIGHT, padx=5)
        self.x_min_scale.set(0)  # Default value

        # X max
        x_max_frame = tk.Frame(generate_window, background="#d4d4d4")
        x_max_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.x_max_label = tk.Label(x_max_frame, text="X max:", background="#d4d4d4")
        self.x_max_label.pack(side=tk.LEFT, padx=5)
        self.x_max_scale = tk.Scale(x_max_frame, from_=0, to=1000, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.x_max_scale.pack(side=tk.RIGHT, padx=5)
        self.x_max_scale.set(1000)  # Default value

        # Y min
        y_min_frame = tk.Frame(generate_window, background="#d4d4d4")
        y_min_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.y_min_label = tk.Label(y_min_frame, text="Y min:", background="#d4d4d4")
        self.y_min_label.pack(side=tk.LEFT, padx=5)
        self.y_min_scale = tk.Scale(y_min_frame, from_=0, to=1000, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.y_min_scale.pack(side=tk.RIGHT, padx=5)
        self.y_min_scale.set(0)  # Default value

        # Y max
        y_max_frame = tk.Frame(generate_window, background="#d4d4d4")
        y_max_frame.pack(pady=5, fill=tk.X, anchor="center")
        self.y_max_label = tk.Label(y_max_frame, text="Y max:", background="#d4d4d4")
        self.y_max_label.pack(side=tk.LEFT, padx=5)
        self.y_max_scale = tk.Scale(y_max_frame, from_=0, to=1000, orient=tk.HORIZONTAL, background="#d4d4d4", width= 10)
        self.y_max_scale.pack(side=tk.RIGHT, padx=5)
        self.y_max_scale.set(1000)  # Default value

        # Generate Button
        self.generate_button = tk.Button(generate_window, text="Generate", command=self.on_generate_random_graph)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        

    def on_generate_random_graph(self):
        print("Generating random graph")
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
        new_graph = random_graph_generator.generate_random_graph(num_points, x_min, x_max, y_min, y_max)
        self.select_graph_type(NONE_GRAPH)  # Sélectionner le type de graphe "Simple Graph"
        self.graph.vertices = new_graph.vertices  # Mettre à jour le graphe dans la barre d'outils
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas
        self.update_vertex_list(self.graph)  # Mettre à jour la liste des sommets dans la barre d'outils


    def update_radius(self):
        self.unit_disk_graph_radius.set(self.graph.radius)


    def show_graph_particularities(self):
        # Clear Frame
        for widget in self.particularities_frame.winfo_children():
            widget.destroy()

        # Rien à afficher si le type de graphe est "None"
        if self.selected_graph_type == UNIT_DISK_GRAPH:
            self.unit_disk_graph_radius = tk.Scale(self.particularities_frame, from_=0, to=200, orient=tk.HORIZONTAL, label="Radius", background="#d4d4d4", command=self.on_radius_change)
            self.update_radius()  # Set the initial value of the scale to the current radius of the graph
            self.unit_disk_graph_radius.pack(pady=5)
            self.show_circle = tk.Checkbutton(self.particularities_frame, text="Show Circles", background="#d4d4d4", command = self.on_circle_check)
            self.show_circle.pack(pady=5)
        # Rien à afficher si le type de graphe est NEAREST_NEIGHBOR_GRAPH

    def on_circle_check(self):
        self.canvas.show_circle_unit_disk_graph = not self.canvas.show_circle_unit_disk_graph  # Inverser l'état de l'affichage des cercles
        print(f"Show circles: {self.canvas.show_circle_unit_disk_graph}")
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

    def on_radius_change(self, value):
        self.graph.set_radius(int(value))  # Mettre à jour le rayon du graphe de disque unitaire
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

    def delete_all(self):
        """
        Supprime tous les sommets du graphe et met à jour la liste des sommets dans la barre d'outils.
        """
        print("Deleting all vertices")
        self.graph.vertices.clear()
        self.graph.linked_points.clear()
        self.vertex_listbox.delete(0, tk.END)  # Effacer la liste des sommets
        self.update_vertex_list(self.graph)  # Mettre à jour la liste des sommets dans la barre d'outils
        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

    def delete_selected_vertex(self):
        """
        Supprime le sommet sélectionné dans la liste et le graphe.
        """
        if self.selected_vertex_index == None: return

        # Supprimer le sommet du graphe
        self.graph.remove_vertex(self.graph.get_vertex_by_index(self.selected_vertex_index))
        self.update_vertex_list(self.graph)
        self.canvas.display_graph(self.graph)
 
    def on_graph_type_select(self, event):
        self.selected_graph_type = self.graph_types_combobox.get()
        print(self.selected_graph_type)

        # remove graph desc test
        self.graph_type_description_text.config(state="normal")
        self.graph_type_description_text.delete("1.0", tk.END)
        self.graph_type_description_text.insert(tk.END, graph_types[self.selected_graph_type])
        self.graph_type_description_text.config(state="disabled")
        print(f"Selected graph type: {self.selected_graph_type}")

        
        if self.selected_graph_type == UNIT_DISK_GRAPH:
            print("Creating Unit Disk Graph")
            self.graph = UnitDiskGraph(self.graph.vertices)
            print(self.graph.vertices)
        elif self.selected_graph_type == NEAREST_NEIGHBOR_GRAPH:
            print("Creating Nearest Neighbour Graph")
            self.graph = NearestNeighbourGraph(self.graph.vertices) 
            print(self.graph.vertices)      
        elif self.selected_graph_type == TRIANGULATION_OF_DELAUNAY_GRAPH:
            print("Creating Delaunay Graph")
            self.graph = Delaunay_graph(self.graph.vertices)
            print(self.graph.vertices)  
        elif self.selected_graph_type == GABRIEL_GRAPH:
            print("Creating Gabriel Graph")
            self.graph = GabrielGraph(self.graph.vertices)
            print(self.graph.vertices)
        else:
            print("Creating Simple Graph")
            self.graph = Graph(vertices = self.graph.vertices)
            print(self.graph.vertices)

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
    
    def on_vertex_select(self, event, vertex_format = None):
        """
        Gère l'événement de sélection d'un sommet dans la liste ou dans le graph.
        :param event: Événement de sélection.
        """
        self.selected_vertex_index = self.vertex_listbox.curselection()[0] if vertex_format is None else vertex_format
        print(f"Selected vertex index: {self.selected_vertex_index}")
        
        vertex = self.vertex_listbox.get(self.selected_vertex_index)
        print(f"Selected vertex: {vertex}")
        # Mettre à jour la couleur du sommet sélectionné dans le canvas
        self.canvas.display_graph(self.graph)

    def get_selected_vertex_index(self):
        """
        Retourne le sommet sélectionné dans la liste.
        :return: Coordonnées du sommet sélectionné.
        """
        return self.selected_vertex_index