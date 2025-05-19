import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
"""Explication : 
    Cette ligne ajoute le répertoire parent du script actuel au chemin de recherche des modules Python.
    Cela permet d'importer des modules qui se trouvent dans le répertoire parent.
"""

from core.graph import Graph
import core.file_manager

from PIL import Image, ImageDraw

def generate_random_graph(n_points, x_min, x_max, y_min, y_max):
    """
    Génère un graphe de n_points points crées aléatoirements avec des coordonnées.
    :param n_points: Number of points to generate.
    :param x_min: Minimum x-coordinate.
    :param x_max: Maximum x-coordinate.
    :param y_min: Minimum y-coordinate.
    :param y_max: Maximum y-coordinate.
    :return: Liste des sommets sous forme de tuples (x, y).
    """
    vertices = [
        (random.randint(x_min, x_max), random.randint(y_min, y_max))
        for _ in range(n_points)
    ]

    new_graph = Graph(vertices)

    return new_graph

def get_graph_image(graph) -> Image:
    """
    Dessine le graphe sur une image
    """
    x_min = min(vertex[0] for vertex in graph.vertices)
    x_max = max(vertex[0] for vertex in graph.vertices)
    y_min = min(vertex[1] for vertex in graph.vertices)
    y_max = max(vertex[1] for vertex in graph.vertices)
    width = x_max - x_min
    height = y_max - y_min

    image = Image.new("RGB", (int(width), int(height)), (255, 255, 255))

    draw = ImageDraw.Draw(image)

    points_offset = [(x - x_min, y - y_min) for x, y in graph.vertices]
    edges_offset = [((edge[0][0] - x_min, edge[0][1] - y_min), (edge[1][0] - x_min, edge[1][1] - y_min)) for edge in graph.linked_points]

    # Affichage des arêtes
    for edge in  edges_offset:
        x1, y1 = edge[0][0], edge[0][1]
        x2, y2 = edge[1][0], edge[1][1]
        draw.line((x1, y1, x2, y2), fill="black", width=1)

    # Affichage des sommets
    for i in range(graph.get_length()):
        vertex = points_offset[i]
        x, y = vertex[0], vertex[1]

        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill = (255, 0, 0))

    return image

def main():
    if len(sys.argv) != 8:
        print("Usage: python graph_generator.py [graph_name] [n_points] [x_min] [x_max] [y_min] [y_max] [file|image|both]")
        sys.exit(1)

    graph_name = sys.argv[1]
    
    n_points = int(sys.argv[2])

    if n_points <= 0:
        print("Number of points must be a positive integer.")
        sys.exit(1)

    try:
        x_min = int(sys.argv[3])
        x_max = int(sys.argv[4])
        y_min = int(sys.argv[5])
        y_max = int(sys.argv[6])
    except ValueError:
        print("Coordinates must be integers.")
        sys.exit(1)

    if x_min >= x_max or y_min >= y_max:
        print("Invalid coordinate ranges.")
        sys.exit(1)

    if sys.argv[7] not in ["file", "image", "both"]:
        print("Invalid output type. Use 'file', 'image' or 'both'.")
        sys.exit(1)
    
    output_type = sys.argv[7]
    graph = generate_random_graph(n_points, x_min, x_max, y_min, y_max)

    print("Generated Random Graph:")
    if output_type == "both":
        print("Output type: both")
        core.file_manager.save_graph_to_json("../graphs/" + graph_name + ".json", graph)
        image = get_graph_image(graph)
        image.save("../graphs/" + graph_name + ".png")
        print(f"Graph file saved to graphs/{graph_name}.json")
        print(f"Graph image saved to graphs/{graph_name}.png")
    elif output_type == "file":
        print("Output type: file")
        core.file_manager.save_graph_to_json("../graphs/" + graph_name + ".json", graph)
        print(f"Graph saved to graphs/{graph_name}.json")

    elif output_type == "image":
        print("Output type: image")
        image = get_graph_image(graph)
        image.save("../graphs/" + graph_name + ".png")
        print(f"Graph image saved to graphs/{graph_name}.png")
        
    

if __name__ == "__main__":
    main()