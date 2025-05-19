from core.graph import Graph
class IntegerGraph(Graph):

    def __init__(self, vertices = []):
        self.vertices =  vertices
        self.linked_points = self.calculate_linked_points()

    def is_integer_distance(self, u, v):
        dist = self.distance(u, v)
        return dist % 1 == 0

    def calculate_linked_points(self):
        linked_points = []
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):

                if self.is_integer_distance(self.vertices[i], self.vertices[j]):
                    linked_points.append((self.vertices[i], self.vertices[j]))
        return linked_points

    