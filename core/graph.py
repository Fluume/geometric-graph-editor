class Graph:
    def  __init__(self):
        self.vertices = [] # Sommets du graphe : un sommet = (x, y)
        self.linked_points = [] # Arrêtes du graphe ( (point1),(point2) )
    
    def get_length(self):
        return len(self.vertices)
    
    def get_vertex_by_index(self, index):
        """Retourne le sommet d'un index donné"""
        return self.vertices[index]

    def add_vertex(self, coord):
        """Ajoute un sommet du graphe"""
        self.vertices.append((coord[0], coord[1]))
    
    def remove_vertex(self, coord):
        """Supprime un sommet du graphe"""
        self.vertices.remove((coord[0], coord[1]))

    def add_linked_points(self, point1, point2):
        """Ajoute une arrête au graphe"""
        self.linked_points.append((point1, point2))

    def remove_linked_points(self, point1, point2):
        """Supprime une arrête au graphe"""
        self.linked_points.remove((point1, point2))
