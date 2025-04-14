import tkinter as tk
import tkinter.ttk as ttk
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # TODO : expliquer

from core.algorithms.unit_disk_graph import UnitDiskGraph
from core.graph import Graph

class Toolbar:
    """
    Classe pour créer une barre d'outils (toolbox) à droite de la fenêtre principale.
    Elle contient des boutons et d'autres éléments d'interface utilisateur.
    """

    def __init__(self, root, graph):
        self.canvas = None  # Référence au canvas (zone de dessin) dans la fenêtre principale
        self.selected_graph_type = "None"  # Type de graphe sélectionné dans la barre d'outils
        # Création d'un panneau (Frame) pour contenir les boutons à droite
        self.frame = tk.Frame(root, background="#d4d4d4", width=400)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.frame.pack_propagate(False)

        self.selected_vertex_index = None  # Variable pour stocker le sommet sélectionné
        self.graph = graph  # Instance de la classe Graph

        # Titre "Toolbox"
        self.label = tk.Label(self.frame, text="Toolbox", font=("Arial", 14), background="#d4d4d4")
        self.label.pack(side=tk.TOP, pady=5)

        """-------------------ELEMENTS-------------------"""

        # Liste des types de graphes
        self.graph_type_label = tk.Label(self.frame, text="Graph Type:", background="#d4d4d4")
        self.graph_type_label.pack(pady=5)

        # Ajouter des types de graphes à la liste
        self.graph_types = {
            "None" : "Simple display of points",
            "Unit Disk Graph" : "It is a graph with one vertex for each disk in the family, and with an edge between two vertices whenever the corresponding vertices lie within a unit distance of each other.",
            "Gabriel Graph (Under development)" : "",
            "Nearest Neighbor Graph (Under development)" : "",
            "Integer Graph (Under development)" : "",
            "k closest-neighbors Graph (Under development)" : "",
            "Minimum Spanning Tree (Under development)" : "",
            "Relative neighborhood graph (Under development)" : "",
            "Triangulation of Delaunay (Under development)" : "",
            "Urquhart graph (Under development)" : "",
            "Theta Graph (Under development)" : "",
            "Yao Graph (Under development)" : "",
            "Yao 4_Linfty (Under development)" : "",
            "TD-Delaunay graph (Under development)" : "",
            "L1-Delaunay graph (Under development)" : "",
            "Demi-Theta6 Graph (Under development)" : "",
        }

        self.graph_types_combobox = ttk.Combobox(self.frame, values = list(self.graph_types.keys()), width=40)
        self.graph_types_combobox.bind("<<ComboboxSelected>>", self.on_graph_type_select)
        self.graph_types_combobox.current(0)
        self.graph_types_combobox.pack(pady=5)
        
        # Description du type de graphe
        self.graph_type_description = tk.Label(self.frame, text="Graph Type Description:", background="#d4d4d4")
        self.graph_type_description.pack(pady=5)

        self.graph_type_description_text = tk.Text(self.frame, height=5, width=40)
        self.graph_type_description_text.pack(pady=5)
        self.graph_type_description_text.insert(tk.END, self.graph_types[self.selected_graph_type])
        self.graph_type_description_text.config(state="disabled")

        

        # Liste des sommets
        self.vertex_label = tk.Label(self.frame, text="Vertices:", background="#d4d4d4")
        self.vertex_label.pack(pady=5)
        
        self.vertex_listbox = tk.Listbox(self.frame, width=30, height=10)
        self.vertex_listbox.pack(pady=5)
        for i in range(graph.get_length()):
            self.vertex_listbox.insert(tk.END, f"{i + 1} | {graph.get_vertex_by_index(i)}")

        self.vertex_listbox.bind("<<ListboxSelect>>", self.on_vertex_select)

        # Bouton pour supprimer un sommet
        self.delete_selected_vertex_button = tk.Button(self.frame, text="Delete Vertex", command=self.delete_selected_vertex)
        self.delete_selected_vertex_button.pack(pady=5)
        # Bouton pour tout supprimer
        self.delete_all_button = tk.Button(self.frame, text="Delete All", command=self.delete_all)
        self.delete_all_button.pack(pady=5) 

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
        self.graph_type_description_text.insert(tk.END, self.graph_types[self.selected_graph_type])
        self.graph_type_description_text.config(state="disabled")
        print(f"Selected graph type: {self.selected_graph_type}")

        
        if self.selected_graph_type == "Unit Disk Graph":
            print("Creating Unit Disk Graph")
            self.graph = UnitDiskGraph(self.graph)
            print(self.graph.vertices)
        else:
            print("Creating Simple Graph")
            self.graph = Graph(vertices = self.graph.vertices)  # Créer un graphe simple avec les sommets existants
            print(self.graph.vertices)
        
        self.canvas.graph = self.graph  # Mettre à jour la référence du graphe dans le canvas

        self.canvas.display_graph(self.graph)  # Mettre à jour l'affichage du graphe sur le canvas

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