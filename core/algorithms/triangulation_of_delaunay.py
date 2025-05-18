from core.graph import Graph

class Delaunay_graph(Graph):
    """
    Classe représentant un graphe de disque unitaire.
    """

    def __init__(self, vertices = []):
        """
        Initialise le graphe avec une liste de sommets.
        :param vertices: Liste de sommets (coordonnées).
        """
        self.vertices = vertices  # Copie des sommets du graphe de base
        self.radius = 100
        self.linked_points = self.calculate_linked_points()


    def mid_point(self, point1, point2, point3):
                    "Enzo et Damien m'ont conseillés le cour de Claude Bernard"
                    """on va calculer le centre du cercle passant par les trois points"""
                    x1, y1 = point1
                    x2, y2 = point2
                    x3, y3 = point3
                    """on vérifie si les trois points sont alignés"""
                    if (x1 - x2) * (y2 - y3) == (y1 - y2) * (x2 - x3):
                        return None
                    # Calcul de les pentes et les ordonnées à l'origine des médiatrices 
                    #(car le centre est le croisement des médiarices du triangle (point1, point2, point3))
                    
                    slope_1_2 = (-(x2+x1)/(y2-y1)) if y2 != y1 else slope_1_2 == 0
                    slope_2_3 = (-(x3+x2)/(y3-y2)) if y3 != y2 else slope_2_3 == 0
                    # Calcul de l'ordonnée à l'origine des médiatrices
                    origin_1_2=((x2**2-x1**2+y2**2-y1**2)/(2*(y2-y1))) if y2 != y1 else origin_1_2 == 0
                    origin_2_3=((x3**2-x2**2+y3**2-y2**2)/(2*(y3-y2))) if y3 != y2 else origin_2_3 == 0
                    # Calcul du centre du cercle
                    x = (origin_2_3 - origin_1_2) / (slope_1_2 - slope_2_3) 
                    y = slope_1_2 * x + origin_1_2
                    return (x, y)

    def calculate_linked_points(self):
        """
        Calcule les arrêtes du graphe en fonction des sommets et de la distance.
        :return: Liste des arrêtes du graphe.
        """
        linked_points = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)): # Évite de vérifier les arrêtes deux fois
                for k in range (i+2, len(self.vertices)): # Évite de vérifier les arrêtes deux fois
                    if k == j:
                        continue
                mid_point = self.mid_point(self.vertices[i], self.vertices[j], self.vertices[k])
                radius=self.distance(mid_point,self .vertices[i])
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

    