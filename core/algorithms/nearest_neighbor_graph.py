from core.graph import Graph

class NearestNeighbourGraph(Graph):
    """
    Classe représentant un graphe des k plus proches voisins (k-NN).
    """

    def __init__(self, vertices = []):
        """
        Initialise le graphe avec les sommets et le nombre k de voisins.
        :param base_graph: Graphe de base contenant les sommets.
        :param k: Nombre de voisins à connecter pour chaque sommet.
        """
        self.vertices =  vertices # Liste de sommets (coordonnées)
        self.linked_points = self.calculate_linked_points()

    def calculate_linked_points(self):
        """
        Calcule les arêtes du graphe en reliant chaque sommet à ses k plus proches voisins.
        :return: Liste des arêtes du graphe.
        """
        linked_points = []
        for point1 in self.vertices:
            # Calculer les distances vers les autres sommets
            distances = []
            for point2 in self.vertices:
                if point1 != point2:
                    distance = self.distance(point1, point2)
                    distances.append((distance, point2))
                

            # Prendre les k plus proches voisins
            nearest_point = distances[0]
            for i in range(1, len(distances)):
                if distances[i][0] < nearest_point[0]:
                    nearest_point = distances[i]
            

            # Ajouter les arêtes (orientées)
            if nearest_point[1] not in linked_points:
                # Vérifier si l'arête n'existe pas déjà
                linked_points.append((point1, nearest_point[1]))
            else:
                # Si l'arête existe déjà, on ne l'ajoute pas
                continue
            linked_points.append((point1, nearest_point[1]))

        return linked_points
