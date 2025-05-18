from core.graph import Graph

class RelativeNeighborhoodGraph(Graph):

    def __init__(self, vertices = []):
        self.vertices = vertices
        self.linked_points = self.calculate_linked_points()

    def calculate_linked_points(self):
        linked_points = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):

                u = self.vertices[i]
                v = self.vertices[j]
                distance_u_v = self.distance(u, v)

                should_link = True
                for k in range(len(self.vertices)):
                    if k == i or k == j:
                        continue

                    w = self.vertices[k]
                    if max(self.distance(u, w), self.distance(v, w)) < distance_u_v:
                        should_link = False
                        break

                if should_link:
                    linked_points.append((u, v))
                    
        return linked_points