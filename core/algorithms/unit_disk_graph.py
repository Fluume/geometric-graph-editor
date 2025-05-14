from core.graph import Graph

class UnitDiskGraph(Graph):
    """
    Classe représentant un graphe de disque unitaire.
    """

    def __init__(self, vertices = []):
        """
        Initialise le graphe avec une liste de sommets.
        :param vertices: Liste de sommets (coordonnées).
        """
        self.vertices =  vertices # Liste de sommets (coordonnées)
        self.radius = 100
        self.linked_points = self.calculate_linked_points()
        

    def calculate_linked_points(self):
        """
        Calcule les arrêtes du graphe en fonction des sommets et de la distance.
        :return: Liste des arrêtes du graphe.
        """
        linked_points = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)): # Évite de vérifier les arrêtes deux fois
                
                if self.distance(self.vertices[i], self.vertices[j]) <= 2 * self.radius:
                    linked_points.append((self.vertices[i], self.vertices[j]))

        return linked_points

    def set_radius(self, radius):
        """
        Définit le rayon du graphe.
        :param radius: Rayon à définir.
        """
        self.radius = radius
        self.linked_points = self.calculate_linked_points()