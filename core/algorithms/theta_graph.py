import math
from core.graph import Graph

class ThetaGraph(Graph):

    def __init__(self, vertices = [], sectors = 6): 
        self.vertices = vertices
        self.sectors = sectors # Nombre de secteurs (cones) autour de chaque point
        self.projection_angle_percent = 0.5 # Angle de la projection (0.5 = milieu du cone)
        self.linked_points = self.calculate_linked_points()
    
    def set_sectors(self, sectors):
        self.sectors = sectors
        self.linked_points = self.calculate_linked_points()

    def set_projection_angle_percent(self, percent):
        self.projection_angle_percent = percent
        self.linked_points = self.calculate_linked_points()

    def calculate_linked_points(self):
        linked_points = []
        for p in self.vertices:
            cones = [[] for i in range(self.sectors)] # Cones autour de p

            # Diviser les points en k secteurs (cones) autour de p
            for q in self.vertices:
                if p == q:
                    continue
                angle = self.angle_between(p, q)

                if angle < 0:
                    angle += 2 * math.pi

                cone_index = int((angle / (2 * math.pi)) * self.sectors) # Trouve dans quel cone se trouve q
                cones[cone_index].append(q)

            # Pour chaque cone, trouver le point le plus proche selon la droite projetée
            for i in range(self.sectors):
                min_q = None
                min_proj_dist = None

                # Direction centrale du cone
                theta = (2 * math.pi * (i + self.projection_angle_percent)) / self.sectors
                dir_vector = (math.cos(theta), math.sin(theta))

                for q in cones[i]:
                    # vecteur p->q
                    vec = (q[0] - p[0], q[1] - p[1])
                    # projection scalaire sur dir_vector
                    proj = vec[0]*dir_vector[0] + vec[1]*dir_vector[1]

                    if min_proj_dist is None or proj < min_proj_dist:
                        min_proj_dist = proj
                        min_q = q

                if min_q is not None:
                    linked_points.append((p, min_q))

        return linked_points


