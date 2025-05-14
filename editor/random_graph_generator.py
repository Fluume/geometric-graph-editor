import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # TODO : expliquer

import core.graph
import core.file_manager

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

    new_graph = core.graph.Graph(vertices)

    return new_graph

def main():
    if len(sys.argv) != 7:
        print("Usage: python random_graph_generator.py graph_name n_points x_min x_max y_min y_max")
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
        
    graph = generate_random_graph(n_points, x_min, x_max, y_min, y_max)

    print("Generated Random Graph:")
    for vertex in graph.vertices:
        print("Vertex:", vertex)

    # Sauvegarder le graphe dans un fichier
    core.file_manager.save_graph_to_json("graphs/" + graph_name + ".json", graph)
    print(f"Graph saved to graphs/{graph_name}.json")

if __name__ == "__main__":
    main()