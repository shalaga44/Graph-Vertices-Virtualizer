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

    def test_add_already_added_vertices_should_return_same_object(self):
        verticesHolders = [VertexHolder(name) for name in self.verticesNamesCollection0]
        newVerticesFirst = self.g.addVerticesHolders(verticesHolders)
        newVerticesSecond = self.g.addVerticesHolders(verticesHolders)
        for first, second in zip(newVerticesFirst, newVerticesSecond):
            self.assertEqual(first, second)

    def test_add_already_added_edges_should_return_same_object(self):
        edgesHolders = [EdgeHolder(start, end) for start, end in self.edgesTupleCollection0]
        newEdgesFirst = self.g.addEdgesHolders(edgesHolders)
        newEdgesSecond = self.g.addEdgesHolders(edgesHolders)
        for first, second in zip(newEdgesFirst, newEdgesSecond):
            self.assertEqual(first, second)


if __name__ == '__main__':
    unittest.main()
