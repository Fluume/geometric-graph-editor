import tkinter as tk
from tkinter import filedialog as fd
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
"""Explication : 
    Cette ligne ajoute le répertoire parent du script actuel au chemin de recherche des modules Python.
    Cela permet d'importer des modules qui se trouvent dans le répertoire parent.
"""

from core.constants import *
import core.file_manager as file_manager
import graph_generator

class GraphMenu:
    def __init__(self, root, graph):
        self.root = root
        self.graph = graph
        self.toolbar = None # L'instance de la barre d'outils sera assignée plus tard dans le main.py
        self.canvas = None # Idem pour le canvas
        menu_bar = tk.Menu(root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New graph", command=self.new_graph_click)
        file_menu.add_command(label="Open graph", command=self.open_graph_click)
        file_menu.add_command(label="Save graph as file", command=self.save_graph_file_click)
        file_menu.add_command(label="Save graph as image", command=self.save_graph_image_click)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # About menu
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About", command=self.on_about_click)
        menu_bar.add_cascade(label="About", menu=about_menu)

        root.config(menu = menu_bar)

    def new_graph_click(self):
        self.toolbar.delete_all()
        self.toolbar.select_graph_type(NONE_GRAPH)

    def open_graph_click(self):
        filetypes = (
            ('Graph files', '*.json'),
        )

        filename = fd.askopenfilename(title='Open a file', initialdir='../graphs/', filetypes=filetypes)

        if not filename:
            print("No file selected")
            return
        
        # Charger le fichier JSON
        loaded_file = file_manager.load_graph_from_json(filename)
        if not loaded_file:
            print("Empty file")
            return
        
        # Vérifier le format du fichier
        if 'vertices' not in loaded_file or 'linked_points' not in loaded_file or 'graph_type' not in loaded_file:
            print("Invalid file format")
            return
        
        # Vérifier le type de graphe
        if loaded_file['graph_type'] not in graph_types:
            print("Invalid graph type")
            return
        
        self.graph.vertices = [(vertex[0], vertex[1]) for vertex in loaded_file['vertices']] # Conversion de liste en tuple
        self.graph.linked_points = loaded_file['linked_points']
        graph_type = loaded_file['graph_type']
        self.toolbar.select_graph_type(loaded_file['graph_type'])
        if graph_type == UNIT_DISK_GRAPH:
            radius = loaded_file['radius']
            print(radius)
            if not isinstance(radius, int) or radius <= 0:
                print("Invalid radius value: radius must be a positive integer")
                return
            self.graph.set_radius(radius)
            self.toolbar.update_radius() 
        elif graph_type == NONE_GRAPH:
            self.graph.linked_points = []
        else:
            print("Invalid graph type")
            return
        
        self.toolbar.update_vertex_list(self.graph)
        self.canvas.display_graph(self.graph)
    
    def save_graph_file_click(self):
        print("Save graph clicked")
        filetypes = (('Graph files', '*.json'),)

        filename = fd.asksaveasfilename(title='Save a graph', initialdir='../graphs/', defaultextension=".json", filetypes=filetypes)

        if not filename:
            print("No file selected")
            return
        
        
        file_manager.save_graph_to_json(filename, graph=self.graph, graph_type=self.toolbar.selected_graph_type)
            
    def save_graph_image_click(self):
        filetypes = (('PNG files', '*.png'),)
        filename = fd.asksaveasfilename(title='Save a graph', initialdir='../graphs/', defaultextension=".json", filetypes=filetypes)

        if not filename:
            print("No file selected")
            return

        image = graph_generator.get_graph_image(self.graph)
        image.save(filename)
        
        print(f"Graph saved as image to {filename}")
        
        


    def on_about_click(self):
        about_window = tk.Toplevel()
        about_window.title("About")
        about_window.geometry("300x200")
        about_label = tk.Label(about_window, text="Graph Editor\nVersion 1.0\nMade with ❤️ by FERRAZZI Tilio and QUENTEL YANN")
        about_label.pack(pady=20)
        about_window.configure(bg="pink")

