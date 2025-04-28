import tkinter as tk
from tkinter import filedialog as fd
import os
import sys
from constants import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # TODO : expliquer
from core.graph import Graph
import core.file_manager as file_manager

class GraphMenu:
    def __init__(self, root, graph):
        self.graph = graph
        self.toolbar = None
        self.canvas = None
        menu_bar = tk.Menu(root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New graph", command=self.new_graph_click)
        file_menu.add_command(label="Open graph", command=self.open_graph_click)
        file_menu.add_command(label="Save graph as", command=self.save_graph_click)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        """
        # Settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="Preferences", command=lambda: print("Open Preferences"))
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        # About menu
        about_menu = tk.Menu(menu_bar, tearoff=0)
        about_menu.add_command(label="About", command=lambda: print("About this application"))
        menu_bar.add_cascade(label="About", menu=about_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Documentation", command=lambda: print("Open Documentation"))
        help_menu.add_command(label="FAQ", command=lambda: print("Open FAQ"))
        menu_bar.add_cascade(label="Help", menu=help_menu)
        """

        # Attach the menu bar to the root window
        root.config(menu=menu_bar)

    def new_graph_click(self):
        print("New graph clicked")
        self.toolbar.delete_all()
        self.toolbar.select_graph_type(NONE_GRAPH)

    def open_graph_click(self):
        filetypes = (
            ('Graph files', '*.json'),
        )

        filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)

        if not filename:
            print("No file selected")
            return
        # Load the graph from the selected file
        loaded_file = file_manager.load_graph_from_json(filename)
        if not loaded_file:
            print("Empty file")
            return
        
        # Verify the loaded file structure
        if 'vertices' not in loaded_file or 'linked_points' not in loaded_file or 'graph_type' not in loaded_file:
            print("Invalid file format")
            return
        
        # Verify the graph type
        if loaded_file['graph_type'] not in graph_types:
            print("Invalid graph type")
            return
        
        self.graph.vertices = loaded_file['vertices']
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
            self.toolbar.update_radius()  # Update the radius in the toolbar
        elif graph_type == NONE_GRAPH:
            self.graph.linked_points = []  # Clear linked points for a simple graph
        else:
            print("Invalid graph type")
            return
        
        self.toolbar.update_vertex_list(self.graph)
        self.canvas.display_graph(self.graph)
    
    def save_graph_click(self):
        print("Save graph clicked")
        filetypes = (
            ('Graph files', '*.json'),
        )

        filename = fd.asksaveasfilename(title='Save a file', initialdir='/', defaultextension=".json", filetypes=filetypes)

        if not filename:
            print("No file selected")
            return
        
        encoded_graph = {
            'vertices': self.graph.vertices,
            'linked_points': self.graph.linked_points,
            'graph_type': self.toolbar.selected_graph_type,
        }
        if self.toolbar.selected_graph_type == UNIT_DISK_GRAPH:
            encoded_graph['radius'] = self.graph.radius # Add the radius to the encoded graph
        
        # Save the graph to the selected file
        file_manager.save_graph_to_json(filename, encoded_graph)
            

