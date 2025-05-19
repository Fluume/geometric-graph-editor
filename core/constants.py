NONE_GRAPH = "None"
UNIT_DISK_GRAPH = "Unit Disk Graph"
GABRIEL_GRAPH = "Gabriel Graph" 
NEAREST_NEIGHBOR_GRAPH = "Nearest Neighbor Graph"
INTEGER_GRAPH = "Integer Graph"
K_CLOSEST_NEIGHBORS_GRAPH = "k closest-neighbors Graph"
MINIMUM_SPANNING_TREE_GRAPH = "Minimum Spanning Tree (in development)"
RELATIVE_NEIGHBORHOOD_GRAPH = "Relative neighborhood graph"
TRIANGULATION_OF_DELAUNAY_GRAPH = "Triangulation of Delaunay"
URQUHART_GRAPH = "Urquhart graph (in development)"
THETA_GRAPH = "Theta Graph"
YAO_GRAPH = "Yao Graph"
YAO_4_LINFTY_GRAPH = "Yao 4_Linfty (in development)"
TD_DELAUNAY_GRAPH = "TD-Delaunay graph (in development)"
L1_DELAUNAY_GRAPH = "L1-Delaunay graph (in development)"
DEMI_THETA6_GRAPH = "Demi-Theta6 Graph (in development)"


graph_types = {
    NONE_GRAPH : "Simple display of points",
    UNIT_DISK_GRAPH : "It is a graph with one vertex for each disk in the family, and with an edge between two vertices whenever the corresponding vertices lie within a unit distance of each other.",
    GABRIEL_GRAPH : "It is a graph where two vertices are connected if the disk whose diameter is the segment joining them contains no other vertex.",
    NEAREST_NEIGHBOR_GRAPH : "It is a graph where each vertex is connected to its nearest neighbor.",
    INTEGER_GRAPH : "It is a graphe where two vertices are connected if they are at an integer distance.",
    K_CLOSEST_NEIGHBORS_GRAPH : "It is a graph where each vertex is connected to its k closest neighbors.",
    MINIMUM_SPANNING_TREE_GRAPH : "In development, none graph is displayed.",
    RELATIVE_NEIGHBORHOOD_GRAPH : "It is a graph where two vertices are connected if there is no other vertex that is closer to both of them than they are to each other.",
    TRIANGULATION_OF_DELAUNAY_GRAPH : "It is a graph where two vertices are connected if the circumcircle of the triangle formed by them contains no other vertex.",
    URQUHART_GRAPH : "In development, none graph is displayed.",
    THETA_GRAPH : "Theta graph is a type of geometric spanner similar to a Yao graph, see https://en.wikipedia.org/wiki/Theta_graph for more details.",
    YAO_GRAPH : " Yao graph is a type of geometric graph similar to a Theta graph, see https://en.wikipedia.org/wiki/Yao_graph for more details.",
    YAO_4_LINFTY_GRAPH : "In development, none graph is displayed.",
    TD_DELAUNAY_GRAPH : "In development, none graph is displayed.",
    L1_DELAUNAY_GRAPH : "In development, none graph is displayed.",
    DEMI_THETA6_GRAPH : "In development, none graph is displayed.",
}
