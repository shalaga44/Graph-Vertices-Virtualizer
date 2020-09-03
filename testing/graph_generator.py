import unittest

from DataTypes.edge_holder import EdgeHolder
from DataTypes.vertex_holder import VertexHolder
from Mangers.graph_generator import GraphGenerator


class MyTestCase(unittest.TestCase):
    g = GraphGenerator(0, 0)
    verticesNamesCollection0 = [0, 1, 2, 3]
    edgesTupleCollection0 = ((0, 1), (1, 2), (2, 3))
    verticesNamesCollection1 = [4, 5, 6, 7]

    def test_add_new_vertices_must_return_them_inOrder(self):
        verticesHolders = [VertexHolder(name) for name in self.verticesNamesCollection0]
        newVertices = self.g.addVerticesHolders(verticesHolders)
        for oldName, newVertex in zip(self.verticesNamesCollection0, newVertices):
            self.assertEqual(str(oldName), newVertex.name)

    def test_add_new_Edges_must_return_them_inOrder(self):
        edgesHolders = [EdgeHolder(start, end) for start, end in self.edgesTupleCollection0]
        newEdges = self.g.addEdgesHolders(edgesHolders)
        for oldTuple, newEdge in zip(self.edgesTupleCollection0, newEdges):
            self.assertEqual(str(oldTuple), str(newEdge))


if __name__ == '__main__':
    unittest.main()
