import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
"""Explication : 
    Cette ligne ajoute le répertoire parent du script actuel au chemin de recherche des modules Python.
    Cela permet d'importer des modules qui se trouvent dans le répertoire parent.
"""

from core.graph import Graph
from core.algorithms.triangulation_of_delaunay_graph import TriangulationOfDelaunayGraph

"""----------------------TESTS-------------------------"""
if __name__ == "__main__":
    graph = Graph()
    print(graph.distance((0, 0), (3, 4))) # 5.0
    print(graph.distance((0, 0), (0, 0))) # 0.0
    print(graph.distance((0, 0), (0, 1))) # 1.0
    print(graph.distance((0, 0), (-1, 0))) # 1.0
    print(graph.distance((0, 0), (1, 1))) # 1.4142135623730951

    print((graph.angle_between((0, 0), (1, 0)))) # 0.0
    print((graph.angle_between((0, 0), (0, 1)))) # 1.5707963267948966
    print((graph.angle_between((0, 0), (-1, 0)))) # 3.141592653589793
    print((graph.angle_between((0, 0), (-1, -1)))) # -2.356194490192345

    delaunay = TriangulationOfDelaunayGraph()

    print(delaunay.mid_point((0, 0), (1, 0), (0, 1))) # (0.5, 0.5)
    print(delaunay.mid_point((0, 0), (1, 0), (1, 1))) # (0.5, 0.5)
    print(delaunay.mid_point((0, 0), (1, 0), (2, 0))) # None