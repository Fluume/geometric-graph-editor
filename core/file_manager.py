import json
from core.constants import *

def save_graph_to_json(file_path, graph, graph_type = NONE_GRAPH):
    """
    Sauvegarde un graphe dans un fichier JSON.

    :param graph: Un dictionnaire représentant le graphe.
    :param file_path: Chemin vers le fichier JSON où le graphe sera sauvegardé.
    :param graph_type: Type de graphe (par défaut : NONE_GRAPH).
    """

    encoded_graph = {
            'vertices': graph.vertices,
            'linked_points': graph.linked_points,
            'graph_type': graph_type,
        }
    
    # Ajout d'attributs spécifiques au type de graphe
    if graph_type == UNIT_DISK_GRAPH:
        encoded_graph['radius'] = graph.radius 
    elif graph_type == THETA_GRAPH:
        encoded_graph['sectors'] = graph.sectors
        encoded_graph['projection_angle_percent'] = graph.projection_angle_percent
    elif graph_type == YAO_GRAPH:
        encoded_graph['sectors'] = graph.sectors
    elif graph_type == K_CLOSEST_NEIGHBORS_GRAPH:
        encoded_graph['k'] = graph.k

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(encoded_graph, file, indent=4)
    except Exception as e:
        print(f"An error occured while saving the graph : {e}")

def load_graph_from_json(file_path):
    """
    Charge un graphe à partir d'un fichier JSON.

    :param file_path: Chemin vers le fichier JSON à partir duquel charger le graphe.
    :return: Un dictionnaire représentant le graphe.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            graph = json.load(file)
        return graph
    except Exception as e:
        print(f"An error occured while loading the graph : {e}")
        return None