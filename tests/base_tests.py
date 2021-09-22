import unittest

from algorithm.base import ShortestPathModel

class preparationTest(unittest.TestCase):
    def setUp(self):
        weights = lambda x,y : abs(x-y)
        self.model = ShortestPathModel(weights)
        self.x = [1 for _ in range(1000)]
        self.y = [0 for _ in range(1000)]

    def test_prpr(self):
        self.model.prepare_data(x, y)
        self.assertEqual(len(self.n_of_labels), len(self.x) + len(self.y))
        