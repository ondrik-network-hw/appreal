
class graph:
    """ This is support class for the PHF functions and others algorithms working on graphs and hypergraphs. It contains only the graph algorithms used in the netbench library. It should behave as a common interface for connecting the netbench pattern matching module to any graph library simply by rewriting these methods. """

    def __init__(self):
        self.vertices = []
        self.edges = []
        self.order = 2

    def set_order(self,order):
        """This function is used to set if this class represent graph or hypergraph. In case of the hypergraph, the order is the number of vertices belonging to the edge. In ordinary graph, order is set to 2. Do not change the order of the graph after inserting the edges or verices into it."""
        self.order = order

    def get_edge_number(self):
        """This function returns the number of edges in the graph"""
        return len(self.edges)

    def get_order(self):
        """ This function returns the order of the hypergraph. See function set_order for more information."""
        return self.order

    def get_vertices_number(self):
        """This function returns number of vertices in the graph. It counts all generated vertices (also vertices without edges). Vertices are named by the number from zero to number of verices."""
        return len(self.vertices)

    def add_vertices(self,number):
        """This function creates given number of verrices and adds them into the graph"""
        start_num = len(self.vertices)
        for i in range(start_num,start_num+number):
             T = vertex(i)
             self.vertices.append(T)

    def get_vertex(self, position):
        """This function returns vertex from graph from the given position"""
        tmp = self.vertices[position]
        return tmp

    def add_edge(self, vertices):
        """This function creates a new edge connecting given vertices. The vertices are given by their numbers (positions).May raise OrderMismatch and OutofRange. The function returns reference to the edge, so the user can set additional rpoperties of the created edge"""
        e = edge(vertices, len(self.edges))
        if e.get_order() != self.order :
            raise OrderMismatch
        #To make sure that degrees are consistent after addign wrong edge
        for i in vertices:
            if i >= len(self.vertices):
                raise OutofRange
        #Increasing degrees of the verices
        #print("EDGE")
        for i in vertices:
            Deg = self.vertices[i].get_degree()
            #print("XXXX",i)
            Deg = Deg + 1
            self.vertices[i].set_degree(Deg)
        self.edges.append(e)
        return e

    def get_edge(self,position):
        """Return n-th edge of the graph. It is usefull for the algorithms requiring to go through all edges of the graph. The order of edges may change by other graph operation. """
        return self.edges[position]
 
    def get_edge_position(self,edge):
        """This function return position of the edge in the graph. It is error if the edge is not in the graph. Positions of edges can be changed by other graph operations."""
        return edge.index

class OrderMismatch(Exception):
    """This exception is generated if the order of edge does is not the same as an order of the graph."""
    def __init__(self):
        return None

class OutofRange(Exception):
    """This exception indicates that the edge is trying to access nonexistent vertex"""
    def __init__(self):
        return None
        

class vertex:
    """This class is used to represent vertices of the graph"""
    def __init__(self,number):
        self.number = number
        self.degree = 0
        self.edges = []

    def get_number(self):
        """This function return unique number of the vertex in the graph"""
        return self.number

    def get_degree(self):
        """Returns the number of the edges corresponding to this vertex (degree of the vertex)"""
        return self.degree

    def set_degree(self, degree):
        """This function sets the degree of the vertex (the number of the edges containing this vertex)"""
        self.degree = degree;

    def add_edge(self,new_edge):
        """Every vertex may store its own edges to accelerate some algorithms. It is user responsibility to create add these edge to the vertex."""
        self.edges.append(new_edge)

    def get_edges(self):
        """This function returns list of edges for the given vertex"""
        return self.edges
        
  
class edge:
    """This class represents the edge of the graph."""
    def __init__(self,vertices, index):
        self.vertices = vertices
        self.index = index

    def get_vertices(self):
        """This function returns list of vertices belonging to the edge. Every vertex is represented by its number"""
        return self.vertices

    def get_order(self):
        """Returns the order of the edge (number of vertices corresponding to the edge)"""
        return len(self.vertices)

