from core.graph import Graph

class NearestNeighbourGraph(Graph):

    def __init__(self, vertices = []):
        self.vertices =  vertices
        self.linked_points = self.calculate_linked_points()

    def calculate_linked_points(self):
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
