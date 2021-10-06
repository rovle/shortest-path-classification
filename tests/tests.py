import unittest

from shpaclass.model import ShortestPathModel

class PreparationTest(unittest.TestCase):
    """Test the prepare_data function."""
    def setUp(self):
        def weights(x,y): return 0
        self.model = ShortestPathModel(weights)
        self.x = [1 for _ in range(100)]
        self.y = [0 for _ in range(100)]
        self.model.prepare_data(self.x, self.y)

    def test_length(self):
        self.assertEqual(self.model.n_of_labels,
                        len(self.x) + len(self.y)
                        )

    def test_flag(self):
        self.assertEqual(self.model.is_data_prepared,
                        True)
    
    def test_sample(self):
        self.assertEqual(self.model.current_sample,
                        self.x + self.y)

    def test_labels(self):
        self.assertEqual(self.model.labels,
                        len(self.x) * [1] + len(self.y) * [0])

class TestAccuracy(unittest.TestCase):
    """Test whether the model computes accuracy accurately."""
    def test_simple(self):
        def weights(x,y): return abs(x-y)

        model = ShortestPathModel(weights)
        x = [1 for _ in range(100)]
        y = [0 for _ in range(100)]
        model.prepare_data(x, y)

        model.fit_predict()

        self.assertEqual(model.accuracy_, 1.0)
    
    def test_complicated(self):
        def weights(x,y): 
            if abs(x-y) < 20:
                return abs(x-y)
            else:
                return float('inf')
        model = ShortestPathModel(weights)
        x = [k for k in range(0, 80)] + [k for k in range(180, 200)]
        y = [k for k in range(80, 181)]
        model.prepare_data(x,y)
        model.fit_predict()

        self.assertEqual(model.accuracy_, 0.8)

class TestGraphConnectedness(unittest.TestCase):
    """Test whether the module handles the graph connectedness correctly."""
    def test_connected(self):
        def weights(x,y): return 0
        x = [1 for _ in range(100)]
        y = [0 for _ in range(100)]
        model = ShortestPathModel(weights)
        model.fit_predict(x+y)

    def test_unconnected(self):
        def weights(x,y): return float('inf')
        x = [1 for _ in range(100)]
        y = [0 for _ in range(100)]
        model = ShortestPathModel(weights)
        with self.assertRaises(Exception):
            model.fit_predict(x+y)