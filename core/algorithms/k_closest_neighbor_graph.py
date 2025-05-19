from core.graph import Graph

class KClosestNeighborGraph(Graph):

    def __init__(self, vertices=[], k=1):
        self.vertices = vertices
        self.k = k # Nombre de voisins les plus proches
        self.linked_points = self.calculate_linked_points()

    def set_k(self, k):
        """
        Définit le nombre de voisins les plus proches à considérer.
        :param k: Nombre de voisins les plus proches.
        """
        if k >= len(self.vertices):
            print("k ne peut pas être supérieur au nombre de sommets.")
            return
        self.k = k
        self.linked_points = self.calculate_linked_points()

    def calculate_linked_points(self):
        if len(self.vertices) < 2:
            print("Pas assez de sommets pour créer un graphe.")
            return []
        
        linked_points = []
        for point1 in self.vertices:
            # Calculer les distances vers les autres sommets
            distances = []
            for point2 in self.vertices:
                if point1 != point2:
                    distance = self.distance(point1, point2)
                    distances.append((distance, point2))
            # Trier les distances et prendre les k plus proches voisins

            distances = sorted(distances, key=lambda x: x[0]) # Tri selon les distances

            for i in range(self.k):
                edge = (point1, distances[i][1])
                # Ajouter l'arête si elle n'existe pas déjà
                if edge not in linked_points:
                    linked_points.append(edge)
        return linked_points