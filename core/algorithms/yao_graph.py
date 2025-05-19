import math
from core.graph import Graph

class YaoGraph(Graph):

    def __init__(self, vertices = [], sectors = 6):
        self.vertices = vertices
        self.sectors = sectors
        self.linked_points = self.calculate_linked_points()

    def set_sectors(self, sectors):
        """
        Définit le nombre de secteurs (cones) autour de chaque point.
        :param sectors: Nombre de secteurs (cones).
        """
        self.sectors = sectors
        self.linked_points = self.calculate_linked_points()

    def calculate_linked_points(self):
        linked_points = []
        for p in self.vertices:
            cones = [[] for i in range(self.sectors)]

            for q in self.vertices:
                if p == q:
                    continue
                angle = self.angle_between(p, q)
                if angle < 0:
                    angle += 2 * math.pi
                cone_index = int((angle / (2 * math.pi)) * self.sectors)
                cones[cone_index].append(q)

            # Dans chaque cone, prendre le point le plus proche (distance euclidienne)
            for i in range(self.sectors):
                min_q = None
                min_dist = None

                for q in cones[i]:
                    dist = self.distance(p, q)
                    if min_dist is None or dist < min_dist:
                        min_dist = dist
                        min_q = q

                if min_q is not None:
                    linked_points.append((p, min_q))

        return linked_points