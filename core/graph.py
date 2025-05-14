class Graph:
    def  __init__(self, vertices = []):
        self.vertices = vertices # Sommets du graphe : un sommet = (x, y)
        self.linked_points = [] # Arrêtes du graphe ( (point1),(point2) )
    
    def get_length(self):
        return len(self.vertices)
    
    def get_vertex_by_index(self, index):
        """Retourne le sommet d'un index donné"""
        return self.vertices[index]

    def add_vertex(self, coord : tuple):
        self.vertices.append((coord[0], coord[1]))
        self.linked_points = self.calculate_linked_points()
    
    def remove_vertex(self, coord):
        self.vertices.remove((coord[0], coord[1]))
        self.linked_points = self.calculate_linked_points()

    def add_linked_points(self, point1, point2):
        self.linked_points.append((point1, point2))

    def remove_linked_points(self, point1, point2):
        self.linked_points.remove((point1, point2))
    
    def distance(self, point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
    
    def calculate_linked_points(self):
        return [] # Pas de liens par défaut