from core.graph import Graph

class TriangulationOfDelaunayGraph(Graph):

    def __init__(self, vertices = []):
        self.vertices = vertices  # Copie des sommets du graphe de base
        self.linked_points = self.calculate_linked_points()


    def mid_point(self, point1, point2, point3):
                    """on va calculer le centre du cercle passant par les trois points"""
                    x1, y1 = point1
                    x2, y2 = point2
                    x3, y3 = point3

                    """on vérifie si les trois points sont alignés"""
                    det = 2 * (x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) # Calcul du déterminant 
                    if det == 0: # Vrai si les points sont alignés
                        return None

                    # Calcul du centre du cercle
                    x = ((x1**2 + y1**2)*(y2 - y3) +
                        (x2**2 + y2**2)*(y3 - y1) +
                        (x3**2 + y3**2)*(y1 - y2)) / det

                    y = ((x1**2 + y1**2)*(x3 - x2) +
                        (x2**2 + y2**2)*(x1 - x3) +
                        (x3**2 + y3**2)*(x2 - x1)) / det

                    return (x, y) # Retourne le centre du cercle

    def calculate_linked_points(self):
        n = len(self.vertices)
        linked_points = []
        for i in range(n):
            for j in range(i + 1, n): # Évite de vérifier les arrêtes deux fois
                for k in range (j +1, n): # Évite de vérifier les arrêtes deux fois
                    center = self.mid_point(self.vertices[i], self.vertices[j], self.vertices[k])
                    if center is None: continue

                    radius = self.distance(center, self.vertices[i])

                    is_valid = True
                    for m in range(n):
                        if m == i or m == j or m == k: continue

                        if self.distance(center, self.vertices[m]) < radius:
                            is_valid = False
                            break
                    
                    if is_valid:
                        linked_points.append((self.vertices[i], self.vertices[j]))
                        linked_points.append((self.vertices[j], self.vertices[k]))
                        linked_points.append((self.vertices[k], self.vertices[i]))

        return linked_points

    