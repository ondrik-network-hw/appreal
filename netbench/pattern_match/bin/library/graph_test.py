import unittest
from graph import *

class BasicGraphTest(unittest.TestCase):
    """This class tests the graph algorithms implemented in the class graph"""

    def testCreateEdge(self):
       """Tests if it is possible to create edge"""
       vertices = [3,2,4]
       Test = edge(vertices)
       self.assert_(Test.get_order() == 3)
       self.assert_(Test.get_vertices() == [3,2,4])

    def testCreateVertex(self):
       """Tests if it is possible to create one vertex"""
       Test = vertex(3)
       self.assert_(Test.get_number() == 3)
       self.assert_(Test.get_degree() == 0)

    def testVertexSetGet(self):
       """Tests setting and getting properties of the Vertex"""
       Test = vertex(3)
       Test.set_degree(3)
       self.assert_(Test.get_degree() == 3)

    def testCreateGraph(self):
       """Tests if it is possible to create instance of the graph"""
       Test = graph()
       self.assert_(Test.get_order() == 2)

    def testSetGetFunctions(self):
       """Tests if it correctly sets properties of the graph"""
       Test = graph()
       Test.set_order(3)
       self.assert_(Test.get_order() == 3)

    def testVertexNumber(self):
       """Test if the number of veritices is returned correctly"""
       Test = graph()
       self.assert_(Test.get_vertices_number() == 0)

    def testAddVertices(self):
       """Tests if it is possoble to add and get vertices from graph"""
       Test = graph()
       Test.add_vertices(4)
       self.assert_(Test.get_vertices_number() == 4)
       Test.add_vertices(8)
       self.assert_(Test.get_vertices_number() == 12)
       for i in range(0,12):
           self.assert_(Test.get_vertex(i).get_number() == i)

    def testSetGraphDegree(self):
       """This function sets the degree of vertex in the graph"""
       Test = graph()
       Test.add_vertices(4)
       Test.get_vertex(2).set_degree(3)
       self.assert_(Test.get_vertex(2).get_degree()==3)
       self.assert_(Test.get_vertex(1).get_degree()==0)
       self.assert_(Test.get_vertex(3).get_degree()==0)

    def testAddEdge(self):
       """Tests adding edge into the graph"""
       Test = graph()
       Test.add_vertices(4)
       Exc = False
       try:
           Test.add_edge([3,2,3,8])
       except OrderMismatch:
           Exc = True
       self.assert_(Exc)
       Test.add_edge([3,2])
       Exc = False
       try:
           Test.add_edge([3,4])
       except OutofRange:
           Exc = True
       self.assert_(Exc)
       self.assert_(Test.get_edge_number() == 1)

    def testVertexEdge(self):
       """Tests addignand getting edges from vertex"""
       Test = vertex(2)
       e = edge([2,2])
       Test.add_edge(e)
       self.assert_(len(Test.get_edges()) == 1)
    
    def testgetEdge(self):
       """Tests if it is possibel to get edge from the graph"""
       Test = graph()
       Test.add_vertices(10)
       Test.add_edge([2,3])
       e = edge([2,3])
       self.assert_(Test.get_edge(0).get_vertices() == [2,3])

    def testGetEdgePosition(self):
       """Tests if it is possible to get edge position in the graph"""
       Test = graph()
       Test.add_vertices(10)
       e1 = Test.add_edge([2,3])
       e2 = Test.add_edge([5,1])
       pos1 = Test.get_edge_position(e1)
       pos2 = Test.get_edge_position(e2)
       self.assert_(e1 == Test.get_edge(pos1))
       self.assert_(e2 == Test.get_edge(pos2))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(BasicGraphTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
