import tkinter as tk
import tkinter.ttk as ttk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # TODO : expliquer

from core.constants import *
from core.algorithms.unit_disk_graph import UnitDiskGraph
from core.algorithms.nearest_neighbor_graph import NearestNeighbourGraph
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

        self.graph_type_description_text = tk.Text(self.settings_label_frame, height=5, width=40)
        self.graph_type_description_text.pack(pady=5)
        self.graph_type_description_text.insert(tk.END, graph_types[self.selected_graph_type])
        self.graph_type_description_text.config(state="disabled")
        
        """---------------------GRAPH PARTICULARITIES---------------------"""
        self.graph_type_particularities = tk.Label(self.settings_label_frame, text="Graph Particularities:", background="#d4d4d4")
        self.graph_type_particularities.pack(pady=5)

        self.particularities_frame = tk.Frame(self.settings_label_frame, background="#d4d4d4")
        self.particularities_frame.pack(pady=5)
        self.show_graph_particularities()

        """---------------------------------------------------------------"""
        

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
        selected_vertex = self.vertex_listbox.curselection()
        if selected_vertex:
            index = selected_vertex[0]
            vertex = self.vertex_listbox.get(index)
            print(f"Deleting vertex: {vertex}")
            # Supprimer le sommet du graphe
            self.graph.remove_vertex(self.graph.get_vertex_by_index(index))
            # Mettre à jour la liste des sommets dans la barre d'outils
            self.update_vertex_list(self.graph)
            # Mettre à jour l'affichage du graphe sur le canvas
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
    
    def on_vertex_select(self, event):
        """
        Gère l'événement de sélection d'un sommet dans la liste.
        :param event: Événement de sélection.
        """
        selected_vertex = self.vertex_listbox.curselection()
        print(f"Selected vertex index: {selected_vertex}")
        if selected_vertex:
            index = selected_vertex[0]
            vertex = self.vertex_listbox.get(index)
            self.selected_vertex_index = selected_vertex[0]
            print(f"Selected vertex: {vertex}")
            # Mettre à jour la couleur du sommet sélectionné dans le canvas
            self.canvas.display_graph(self.graph)

    def get_selected_vertex_index(self):
        """
        Retourne le sommet sélectionné dans la liste.
        :return: Coordonnées du sommet sélectionné.
        """
        return self.selected_vertex_index