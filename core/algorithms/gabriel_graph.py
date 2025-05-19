from core.graph import Graph

class GabrielGraph(Graph):

    def __init__(self, vertices = []):
        self.vertices = vertices
        self.linked_points = self.calculate_linked_points()


    def calculate_linked_points(self):
        linked_points = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)): # Évite de vérifier les arrêtes deux fois
                mid_point= ((self.vertices[i][0] + self.vertices[j][0]) / 2, (self.vertices[i][1] + self.vertices[j][1]) / 2)
                radius = self.distance(self.vertices[i], self.vertices[j]) / 2
                # Vérifie si tous les autres sommets sont à une distance supérieure au rayon
                for k in range(len(self.vertices)):
                    if k != i and k != j:
                        if self.distance(mid_point, self.vertices[k]) < radius:
                            break
                else:  # Si la boucle n'a pas été interrompue, ajoute l'arrête
                    linked_points.append((self.vertices[i], self.vertices[j]))
        return linked_points
